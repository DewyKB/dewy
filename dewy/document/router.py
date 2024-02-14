from typing import Annotated, List, Union

import asyncpg
from fastapi import (
    APIRouter,
    BackgroundTasks,
    File,
    HTTPException,
    Path,
    Query,
    UploadFile,
    status,
)
from loguru import logger

from dewy.common.collection_embeddings import (
    CollectionEmbeddings,
    IngestContent,
    IngestURL,
)
from dewy.common.db import PgConnectionDep, PgPoolDep
from dewy.config import Config, ConfigDep
from dewy.document.models import Document

from .models import AddDocumentRequest, DocumentStatus

router = APIRouter(prefix="/documents")


async def ingest_document(
    document_id: int,
    pg_pool: asyncpg.Pool,
    config: Config,
    request: Union[IngestContent, IngestURL],
) -> None:
    try:
        if isinstance(request, IngestURL) and request.url.startswith("error://"):
            raise RuntimeError(request.url.removeprefix("error://"))
        embeddings = await CollectionEmbeddings.for_document_id(pg_pool, config, document_id)
        await embeddings.ingest(document_id, request)
    except Exception as e:
        logger.error("Failed to ingest {}: {}", document_id, e)
        async with pg_pool.acquire() as conn:
            async with conn.transaction():
                logger.info("Deleting embeddings for failed document {}", document_id)
                await conn.execute(
                    """
                    DELETE FROM embedding
                    USING chunk
                    WHERE chunk.document_id = $1
                    AND embedding.chunk_id = chunk.id
                    """,
                    document_id,
                )
                logger.info("Deleting chunks for failed document {}", document_id)
                await conn.execute(
                    """
                    DELETE FROM chunk
                    WHERE document_id = $1
                    RETURNING id
                    """,
                    document_id,
                )
                logger.info("Updating status of failed document {}", document_id)
                await conn.execute(
                    """
                    UPDATE document
                    SET
                        ingest_state = 'failed',
                        ingest_error = $2
                    WHERE id = $1
                    """,
                    document_id,
                    str(e),
                )


@router.post("/")
async def add_document(
    pg_pool: PgPoolDep,
    config: ConfigDep,
    background: BackgroundTasks,
    req: AddDocumentRequest,
) -> Document:
    """Add a document from a URL."""
    async with pg_pool.acquire() as conn:
        row = None
        try:
            row = await conn.fetchrow(
                """
                INSERT INTO document (collection_id, url, ingest_state)
                VALUES ((SELECT id FROM collection WHERE lower(name) = lower($1)), $2, 'pending')
                RETURNING id, collection_id, url, ingest_state, ingest_error, $1 AS collection
                """,
                req.collection,
                req.url,
            )
        except asyncpg.NotNullViolationError as e:
            if e.column_name == "collection_id":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No collection named '{req.collection}'",
                )
            else:
                raise e from None

    document = Document.model_validate(dict(row))

    if req.url:
        background.add_task(ingest_document, document.id, pg_pool, config, IngestURL(url=req.url))
    return document


# We can't accept the collection ID in a body parameter, since it conflicts with
# the content payload and breaks in at least the Python client generator.
@router.post("/{document_id}/content")
async def upload_document_content(
    pg_pool: PgPoolDep,
    config: ConfigDep,
    background: BackgroundTasks,
    document_id: Annotated[int, Path(description="The collection to add the document to.")],
    content: Annotated[UploadFile, File(description="The document content.")],
) -> Document:
    """Add a document from specific content."""

    # The upload file is in a spooled tepmorary file. This means it is in memory
    # if it is a small file, and on disk if it was larger. However, the upload file
    # we receive will also be closed at the end of the request handler, so we need
    # to either read it into memory or copy it to a file.
    #
    # See https://github.com/tiangolo/fastapi/discussions/10936

    if not content.size:
        raise HTTPException(status.HTTP_412_PRECONDITION_FAILED, "Missing content size")
    SIZE_LIMIT = 50_000_000
    if content.size > SIZE_LIMIT:
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            f"Content size {content.size} exceeds limit of {SIZE_LIMIT} bytes",
        )

    document = None
    async with pg_pool.acquire() as conn:
        document = await get_document(conn, document_id)

    content_bytes = await content.read()
    background.add_task(
        ingest_document,
        document.id,
        pg_pool,
        config,
        IngestContent(
            filename=content.filename,
            content_type=content.content_type,
            size=content.size,
            content_bytes=content_bytes,
        ),
    )
    return document


PathDocumentId = Annotated[int, Path(..., description="The document ID.")]


@router.get("/")
async def list_documents(
    conn: PgConnectionDep,
    collection: Annotated[
        str | None,
        Query(description="Limit to documents associated with this collection"),
    ] = None,
) -> List[Document]:
    """List documents."""
    # TODO: Test
    results = await conn.fetch(
        """
        SELECT d.id, c.name AS collection, d.url, d.ingest_state, d.ingest_error
        FROM document d
        JOIN collection c ON c.id = d.collection_id
        WHERE lower(c.name) = coalesce(lower($1), lower(c.name))
        """,
        collection,
    )

    return [Document.model_validate(dict(result)) for result in results]


@router.get("/{id}")
async def get_document(conn: PgConnectionDep, id: PathDocumentId) -> Document:
    result = await conn.fetchrow(
        """
        SELECT d.id, c.name AS collection, d.url, d.ingest_state, d.ingest_error, d.extracted_text
        FROM document d
        JOIN collection c ON d.collection_id = c.id
        WHERE d.id = $1
        """,
        id,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No document with ID {id}"
        )
    return Document.model_validate(dict(result))


@router.get("/{id}/status")
async def get_document_status(conn: PgConnectionDep, id: PathDocumentId) -> DocumentStatus:
    result = await conn.fetchrow(
        """
        SELECT ingest_state, ingest_error
        FROM document
        WHERE id = $1
        """,
        id,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No document with ID {id}"
        )
    return DocumentStatus(
        id=id, ingest_state=result["ingest_state"], ingest_error=result["ingest_error"]
    )

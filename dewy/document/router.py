from typing import Annotated, List

import asyncpg
from fastapi import APIRouter, BackgroundTasks, Path, Query
from loguru import logger

from dewy.common.collection_embeddings import CollectionEmbeddings
from dewy.common.db import PgConnectionDep, PgPoolDep
from dewy.document.models import Document

from .models import AddDocumentContentRequest, AddDocumentRequest, AddDocumentUrlRequest, DocumentStatus

router = APIRouter(prefix="/documents")


async def ingest_document(document_id: int, pg_pool: asyncpg.Pool) -> None:
    try:
        url, embeddings = await CollectionEmbeddings.for_document_id(
            pg_pool, document_id
        )
        if url.startswith("error://"):
            raise RuntimeError(url.removeprefix("error://"))
        await embeddings.ingest(document_id, url)
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


@router.post("/url")
async def add_document_from_url(
    pg_pool: PgPoolDep,
    background: BackgroundTasks,
    req: AddDocumentUrlRequest
) -> Document:
    """Add a document from a URL."""
    async with pg_pool.acquire() as conn:
        row = None
        row = await conn.fetchrow(
            """
        INSERT INTO document (collection_id, url, ingest_state)
        VALUES ($1, $2, 'pending')
        RETURNING id, collection_id, url, ingest_state, ingest_error
        """,
            req.collection_id,
            req.url,
        )

    document = Document.model_validate(dict(row))
    background.add_task(ingest_document, document.id, pg_pool)
    return document

@router.post("/content")
async def add_document_from_content(
    pg_pool: PgPoolDep,
    background: BackgroundTasks,
    req: AddDocumentContentRequest
) -> Document:
    """Add a document from specific content."""
    pass

PathDocumentId = Annotated[int, Path(..., description="The document ID.")]


@router.get("/")
async def list_documents(
    conn: PgConnectionDep,
    collection_id: Annotated[
        int | None,
        Query(description="Limit to documents associated with this collection"),
    ] = None,
) -> List[Document]:
    """List documents."""
    # TODO: Test
    if collection_id is None:
        results = await conn.fetch(
            """
            SELECT id, collection_id, url, ingest_state, ingest_error
            FROM document
        """
        )
    else:
        results = await conn.fetch(
            """
            SELECT id, collection_id, url, ingest_state, ingest_error
            FROM document WHERE collection_id = $1
        """,
            collection_id,
        )
    return [Document.model_validate(dict(result)) for result in results]


@router.get("/{id}")
async def get_document(conn: PgConnectionDep, id: PathDocumentId) -> Document:
    # TODO: Test / return not found?
    result = await conn.fetchrow(
        """
        SELECT id, collection_id, url, ingest_state, ingest_error, extracted_text
        FROM document WHERE id = $1
        """,
        id,
    )
    return Document.model_validate(dict(result))


@router.get("/{id}/status")
async def get_document_status(
    conn: PgConnectionDep, id: PathDocumentId
) -> DocumentStatus:
    result = await conn.fetchrow(
        """
        SELECT ingest_state, ingest_error
        FROM document
        WHERE id = $1
        """,
        id,
    )
    return DocumentStatus(
        id=id, ingest_state=result["ingest_state"], ingest_error=result["ingest_error"]
    )

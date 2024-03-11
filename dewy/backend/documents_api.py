from typing import Annotated, List, Optional

import pydantic
from fastapi import (
    APIRouter,
    File,
    HTTPException,
    Path,
    Query,
    Response,
    UploadFile,
    status,
)

from dewy.domain import chunks, documents
from dewy.domain.ingest import (
    IngestContent,
    IngestURL,
)

from ._dependencies import DewyTasksDep, PgConnectionDep

router = APIRouter(prefix="/documents")


class AddDocumentRequest(pydantic.BaseModel):
    collection: str = pydantic.Field(..., examples=["main"])
    """The id of the collection the document should be added to."""

    url: Optional[str] = None
    """The URL of the document to add.

    If not specified, content may be uploaded later.
    """


@router.post("/")
async def add_document(
    req: AddDocumentRequest,
    conn: PgConnectionDep,
    tasks: DewyTasksDep,
) -> documents.Document:
    """Add a document to a collection."""
    document = await documents.add_document(
        conn,
        collection=req.collection,
        url=req.url,
    )

    # If there is a URL, kick off an ingestion.
    if req.url:
        await tasks.ingest.kiq(document_id=document.id, request=IngestURL(url=req.url))

    return document


# We can't accept the collection ID in a body parameter, since it conflicts with
# the content payload and breaks in at least the Python client generator.
@router.post("/{document_id}/content")
async def upload_document_content(
    document_id: Annotated[int, Path(description="The collection to add the document to.")],
    content: Annotated[UploadFile, File(description="The document content.")],
    tasks: DewyTasksDep,
    conn: PgConnectionDep,
) -> documents.Document:
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

    async with conn.transaction():
        await chunks.remove_chunks_for_document(conn, document_id)
        await documents.update_status(conn, document_id, documents.IngestState.PENDING)

    result = await documents.get_document(conn, document_id)
    assert result.ingest_state == documents.IngestState.PENDING

    content_bytes = await content.read()
    await tasks.ingest.kiq(
        document_id=document_id,
        request=IngestContent(
            filename=content.filename,
            content_type=content.content_type,
            size=content.size,
            content_bytes=content_bytes,
        ),
    )
    return result


@router.get("/")
async def list_documents(
    conn: PgConnectionDep,
    collection: Annotated[
        str | None,
        Query(description="Limit to documents associated with this collection"),
    ] = None,
) -> List[documents.Document]:
    """List documents."""
    return await documents.list_documents(conn, collection)


@router.get("/{id}")
async def get_document(
    conn: PgConnectionDep, id: Annotated[int, Path(..., description="The document ID.")]
) -> documents.Document:
    return await documents.get_document(conn, id)


@router.get(
    "/{id}/status", response_model_include=["id", "collection", "ingest_state", "ingest_error"]
)
async def get_document_status(
    conn: PgConnectionDep, id: Annotated[int, Path(..., description="The document ID.")]
) -> documents.Document:
    return await documents.get_document(conn, id)


@router.delete("/{id}")
async def delete_document(
    conn: PgConnectionDep, id: Annotated[int, Path(..., description="The document ID.")]
):
    """Delete a document."""

    await documents.delete(conn, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

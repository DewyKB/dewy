from typing import Annotated, List

import asyncpg
from fastapi import APIRouter, BackgroundTasks, Path, Query

from dewy.common.collection_embeddings import CollectionEmbeddings
from dewy.common.db import PgConnectionDep, PgPoolDep
from dewy.document.models import Document

from .models import AddDocumentRequest

router = APIRouter(prefix="/documents")


async def ingest_document(document_id: int, pg_pool: asyncpg.Pool) -> None:
    url, embeddings = await CollectionEmbeddings.for_document_id(pg_pool, document_id)
    await embeddings.ingest(document_id, url)


@router.put("/")
async def add_document(
    pg_pool: PgPoolDep,
    background: BackgroundTasks,
    req: AddDocumentRequest,
) -> Document:
    """Add a document."""

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
        SELECT id, collection_id, url, ingest_state, ingest_error
        FROM document WHERE id = $1
        """,
        id,
    )
    return Document.model_validate(dict(result))

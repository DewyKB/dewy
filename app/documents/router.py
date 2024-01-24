from typing import Annotated, List

import asyncpg
from fastapi import APIRouter, BackgroundTasks, Body, HTTPException, Path, status
from loguru import logger

from app.collections.router import PathCollectionId
from app.common.db import PgConnectionDep, PgPoolDep
from app.documents.models import Document
from app.ingest.extract import extract
from app.ingest.extract.source import ExtractSource
from app.ingest.store import Store, StoreDep

# TODO: Move this to `/documents`. Will require figuring out
# how to specify the collection for create, list, etc.
router = APIRouter(prefix="/collections/{collection_id}/documents")


# We can't use the session from the request because it ends as soon
# as the request completes. So we need to pass the engine and start
# a new session.
async def ingest_document(id: int, store: Store, pg_pool: asyncpg.Pool):
    # Load the content.
    async with pg_pool.acquire() as conn:
        url = await conn.fetchval("SELECT url FROM document WHERE id = $1", id)

        logger.debug("Loading content for document {} from {}", id, url)
        documents = await extract(
            ExtractSource(
                url,
            )
        )
        logger.debug("Loaded {} pages from {}", len(documents), url)
        if not documents:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail=f"No content retrieved from '{url}'",
            )

        logger.debug("Inserting {} documents from {}", len(documents), url)
        nodes = await store.ingestion_pipeline.arun(documents=documents)
        logger.debug("Done. Inserted {} nodes", len(nodes))

        await conn.execute(
            """
        UPDATE document
        SET ingest_state = 'ingested', ingest_error = NULL
        WHERE id = $1
        """,
            id,
        )


@router.put("/")
async def add_document(
    collection_id: PathCollectionId,
    store: StoreDep,
    pg_pool: PgPoolDep,
    background: BackgroundTasks,
    url: Annotated[str, Body(..., description="The URL of the document to add.")],
) -> Document:
    """Add a document."""

    row = None
    async with pg_pool.acquire() as conn:
        row = await conn.fetchrow(
            """
        INSERT INTO document (collection_id, url, ingest_state)
        VALUES ($1, $2, 'pending')
        RETURNING id, collection_id, url, ingest_state, ingest_error
        """,
            collection_id,
            url,
        )

    document = Document.model_validate(dict(row))
    background.add_task(ingest_document, document.id, store, pg_pool)
    return document


PathDocumentId = Annotated[int, Path(..., description="The document ID.")]


@router.get("/")
async def list_documents(
    collection_id: PathCollectionId, conn: PgConnectionDep
) -> List[Document]:
    """List documents."""
    # TODO: Test
    results = await conn.fetch(
        """
        SELECT id, collection_id, url, ingest_state, ingest_error
        FROM document WHERE collection_id = $1
    """,
        collection_id,
    )
    return [Document.model_validate(dict(result)) for result in results]


@router.get("/{id}")
async def get_document(
    conn: PgConnectionDep, collection_id: PathCollectionId, id: PathDocumentId
) -> Document:
    # TODO: Test / return not found?
    result = await conn.fetchrow(
        """
        SELECT id, collection_id, url, ingest_state, ingest_error
        FROM document WHERE id = $1 AND collection_id = $2
        """,
        id,
        collection_id,
    )
    return Document.model_validate(dict(result))

from typing import Annotated, List

import asyncpg
from fastapi import APIRouter, BackgroundTasks, Body, HTTPException, Path, status, Query
from loguru import logger

from app.common.db import PgConnectionDep, PgPoolDep
from app.documents.models import Document
from app.ingest.extract import extract
from app.ingest.extract.source import ExtractSource
from app.ingest.store import Store, StoreDep

from .models import CreateRequest

router = APIRouter(prefix="/documents")

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
    store: StoreDep,
    pg_pool: PgPoolDep,
    background: BackgroundTasks,
    req: CreateRequest,
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
            req.collection_id,
            req.url,
        )

    document = Document.model_validate(dict(row))
    background.add_task(ingest_document, document.id, store, pg_pool)
    return document


PathDocumentId = Annotated[int, Path(..., description="The document ID.")]


@router.get("/")
async def list_documents(
    conn: PgConnectionDep,
    collection_id: Annotated[int | None, Query(description="Limit to documents associated with this collection")] = None,
) -> List[Document]:
    """List documents."""
    # TODO: Test
    if collection_id == None:
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
async def get_document(
    conn: PgConnectionDep, id: PathDocumentId
) -> Document:
    # TODO: Test / return not found?
    result = await conn.fetchrow(
        """
        SELECT id, collection_id, url, ingest_state, ingest_error
        FROM document WHERE id = $1
        """,
        id,
    )
    return Document.model_validate(dict(result))

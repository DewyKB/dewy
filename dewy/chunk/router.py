from typing import Annotated, List

from fastapi import APIRouter, Path, Query
from loguru import logger

from dewy.common.collection_embeddings import CollectionEmbeddings
from dewy.common.db import PgPoolDep
from dewy.config import ConfigDep

from .models import Chunk, RetrieveRequest, RetrieveResponse, TextChunk

router = APIRouter(prefix="/chunks")


@router.get("/")
async def list_chunks(
    pg_pool: PgPoolDep,
    collection: Annotated[
        str | None, Query(description="Limit to chunks associated with this collection")
    ] = None,
    document_id: Annotated[
        int | None, Query(description="Limit to chunks associated with this document")
    ] = None,
    page: int | None = 0,
    perPage: int | None = 10,
) -> List[Chunk]:
    """List chunks."""

    # TODO: handle collection & document ID
    perPage = perPage or 10
    page = page or 0
    limit = perPage
    offset = page * perPage
    results = await pg_pool.fetch(
        """
        SELECT k.id, k.document_id, k.kind, TRUE as raw, k.text
        FROM chunk k
        JOIN document d ON d.id = k.document_id
        JOIN collection c ON d.collection_id = c.id
        WHERE lower(c.name) = coalesce(lower($1), lower(c.name))
        AND k.document_id = coalesce($2, k.document_id)
        ORDER BY k.id
        OFFSET $3
        LIMIT $4
        """,
        collection,
        document_id,
        offset,
        limit,
    )
    logger.info("Retrieved {} chunks", len(results))
    return [TextChunk.model_validate(dict(result)) for result in results]


PathChunkId = Annotated[int, Path(..., description="The chunk ID.")]


@router.get("/{id}")
async def get_chunk(
    pg_pool: PgPoolDep,
    id: PathChunkId,
) -> Chunk:
    # TODO: Test / return not found?
    result = await pg_pool.fetchrow(
        """
        SELECT id, document_id, kind, text
        FROM chunk WHERE id = $1
        """,
        id,
    )
    return Chunk.model_validate(dict(result))


@router.post("/retrieve")
async def retrieve_chunks(
    pg_pool: PgPoolDep, config: ConfigDep, request: RetrieveRequest
) -> RetrieveResponse:
    """Retrieve chunks based on a given query."""

    # TODO: Revisit response synthesis and hierarchical fetching.

    collection = await CollectionEmbeddings.for_collection(pg_pool, config, request.collection)
    text_results = await collection.retrieve_text_chunks(query=request.query, n=request.n)

    return RetrieveResponse(
        summary=None,
        text_results=text_results if request.include_text_chunks else [],
        image_results=[],
    )

from typing import Annotated, List

from fastapi import APIRouter, Path, Query

from dewy.common.collection_embeddings import CollectionEmbeddings
from dewy.common.db import PgPoolDep

from .models import Chunk, RetrieveRequest, RetrieveResponse, TextChunk

router = APIRouter(prefix="/chunks")


@router.get("/")
async def list_chunks(
    pg_pool: PgPoolDep,
    collection_id: Annotated[
        int | None, Query(description="Limit to chunks associated with this collection")
    ] = None,
    document_id: Annotated[
        int | None, Query(description="Limit to chunks associated with this document")
    ] = None,
    page: int | None = 1,
    perPage: int | None = 10,
) -> List[Chunk]:
    """List chunks."""

    # TODO: handle collection & document ID
    results = await pg_pool.fetch(
        """
        SELECT chunk.id, chunk.document_id, chunk.kind, TRUE as raw, chunk.text
        FROM chunk
        JOIN document ON document.id = chunk.document_id
        WHERE document.collection_id = coalesce($1, document.collection_id)
        AND chunk.document_id = coalesce($2, chunk.document_id)
        ORDER BY chunk.id
        OFFSET $4
        LIMIT $3
        """,
        collection_id,
        document_id,
        perPage,
        page,
    )
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
    pg_pool: PgPoolDep, request: RetrieveRequest
) -> RetrieveResponse:
    """Retrieve chunks based on a given query."""

    # TODO: Revisit response synthesis and hierarchical fetching.

    collection = await CollectionEmbeddings.for_collection_id(
        pg_pool, request.collection_id
    )
    text_results = await collection.retrieve_text_chunks(
        query=request.query, n=request.n
    )

    return RetrieveResponse(
        summary=None,
        text_results=text_results if request.include_text_chunks else [],
        image_results=[],
    )

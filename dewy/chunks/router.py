from fastapi import APIRouter

from dewy.common.collection_embeddings import CollectionEmbeddings
from dewy.common.db import PgPoolDep

from .models import RetrieveRequest, RetrieveResponse

router = APIRouter(prefix="/chunks")


@router.post("/retrieve")
async def retrieve_chunks(
    pg_pool: PgPoolDep, request: RetrieveRequest
) -> RetrieveResponse:
    """Retrieve chunks based on a given query."""

    # TODO: Revisit response synthesis and hierarchical fetching.

    collection = await CollectionEmbeddings.for_collection_id(
        pg_pool, request.collection_id
    )
    chunks = await collection.retrieve_text_chunks(query=request.query, n=request.n)

    return RetrieveResponse(summary=None, chunks=chunks)

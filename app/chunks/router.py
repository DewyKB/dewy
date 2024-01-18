from fastapi import APIRouter
from loguru import logger

from app.common.models import Chunk, RetrieveRequest
from app.ingest.store import StoreDep

from .models import RetrieveResponse

router = APIRouter(tags=["chunks"], prefix="/chunks")


@router.post("/retrieve")
async def retrieve(store: StoreDep, request: RetrieveRequest) -> RetrieveResponse:
    """Retrieve chunks based on a given query."""

    logger.info("Retrieving chunks for query:", request)
    results = store.index.as_query_engine(
        similarity_top_k=request.n,
        response_mode=request.synthesis_mode.value,
        # TODO: metadata filters / ACLs
    ).query(request.query)

    chunks = [Chunk.from_llama_index(node) for node in results.source_nodes]
    return RetrieveResponse(
        synthesized_text=results.response,
        chunks=chunks,
    )

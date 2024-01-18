from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status
from loguru import logger

from app.common.models import RetrieveRequest
from app.documents.models import RetrieveResponse
from app.ingest.extract import extract
from app.ingest.extract.source import ExtractSource
from app.ingest.store import StoreDep

router = APIRouter(tags=["documents"], prefix="/documents")

@router.put("/")
async def add(
    store: StoreDep,
    url: Annotated[str, Body(..., description="The URL of the document to add.")],
):
    """Add a document."""

    # Load the content.
    logger.debug("Loading content from {}", url)
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

@router.post("/retrieve")
async def retrieve(
    _store: StoreDep, _request: RetrieveRequest
) -> RetrieveResponse:
    """Retrieve documents based on a given query."""
    raise NotImplementedError()
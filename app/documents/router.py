from typing import Annotated, List

from fastapi import APIRouter, BackgroundTasks, Body, HTTPException, Path, status
from loguru import logger
from sqlalchemy import Engine
from sqlmodel import Session, select

from app.common.schema import Document, EngineDep, IngestState
from app.ingest.extract import extract
from app.ingest.extract.source import ExtractSource
from app.ingest.store import Store, StoreDep

router = APIRouter(tags=["documents"], prefix="/documents")


async def ingest_document(id: int, store: Store, engine: Engine):
    # Load the content.
    with Session(engine) as session:
        document = session.get(Document, id)

        logger.debug("Loading content from {}", document.url)
        documents = await extract(
            ExtractSource(
                document.url,
            )
        )
        logger.debug("Loaded {} pages from {}", len(documents), document.url)
        if not documents:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail=f"No content retrieved from '{document.url}'",
            )

        logger.debug("Inserting {} documents from {}", len(documents), document.url)
        nodes = await store.ingestion_pipeline.arun(documents=documents)
        logger.debug("Done. Inserted {} nodes", len(nodes))

        document.ingest_state = IngestState.INGESTED
        document.ingest_error = None
        session.add(document)
        session.commit()

@router.put("/")
async def add(
    store: StoreDep,
    engine: EngineDep,
    background: BackgroundTasks,
    url: Annotated[str, Body(..., description="The URL of the document to add.")],
) -> Document:
    """Add a document."""

    # Update the document in the DB.
    document = Document(
        url = url
    )
    with Session(engine) as session:
        # TODO: Support update (and fail if the document doesn't exist/etc.)

        document.ingest_state = IngestState.PENDING
        document.ingest_error = None

        session.add(document)
        session.commit()
        session.refresh(document)

        # Create the background task to update the state.
        background.add_task(ingest_document, document.id, store, engine)

    return document

PathDocumentId = Annotated[int, Path(..., description="The document ID.")]

@router.get("/")
async def list(engine: EngineDep) -> List[Document]:
    """List documents."""
    with Session(engine) as session:
        return session.exec(select(Document)).all()

@router.get("/{id}")
async def get(
    engine: EngineDep,
    id: PathDocumentId
) -> Document:
    with Session(engine) as session:
        return session.get(Document, id)

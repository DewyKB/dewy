from enum import Enum
from typing import Annotated, Optional

from fastapi import Depends, Request
from sqlalchemy import Engine, UniqueConstraint
from sqlmodel import Field, SQLModel


class Collection(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # TODO: We may want this to be unique per-tenant rather than globally unique names.
    name: str = Field(index=True, unique=True)

class IngestState(Enum):
    UNKNOWN = "unknown"
    """Document is in an unknown state."""

    PENDING = "pending"
    """Document is pending ingestion."""

    INGESTED = "ingested"
    """Document has been ingested."""

    FAILED = "failed"
    """Document failed to be ingested. See `ingest_errors` for details."""

class Document(SQLModel, table=True):
    """Schema for documents in the SQL DB."""

    __table_args__ = (
        UniqueConstraint("collection_id", "url"),
        UniqueConstraint("collection_id", "doc_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    collection_id: Optional[int] = Field(foreign_key="collection.id")

    url: str = Field(index=True)
    doc_id: Optional[str] = Field(default=None)

    ingest_state: IngestState = Field(default=IngestState.UNKNOWN)
    """The state of the document ingestion."""

    ingest_error: Optional[str] = Field(default=None)
    """Errors which occurred during ingestion, if any."""


def _db(request: Request) -> Engine:
    return request.state.engine


EngineDep = Annotated[Engine, Depends(_db)]

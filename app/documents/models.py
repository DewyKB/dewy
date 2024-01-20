from enum import Enum
from typing import Optional

from pydantic import BaseModel


class IngestState(Enum):
    PENDING = "pending"
    """Document is pending ingestion."""

    INGESTED = "ingested"
    """Document has been ingested."""

    FAILED = "failed"
    """Document failed to be ingested. See `ingest_errors` for details."""

class Document(BaseModel):
    """Schema for documents in the SQL DB."""

    id: Optional[int] = None
    collection_id: int

    url: str

    ingest_state: Optional[IngestState] = None
    ingest_error: Optional[str] = None
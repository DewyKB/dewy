from enum import Enum
from typing import Optional, Union
from fastapi import UploadFile

from pydantic import BaseModel

class AddDocumentUrlRequest(BaseModel):
    collection_id: int
    """The id of the collection the document should be added to."""

    url: str
    """The URL of the document to add."""

class AddDocumentContentRequest(BaseModel):
    collection_id: int
    """The id of the collection the docuemnt should be added to."""

    content: Union[str, UploadFile]
    """The content to use for the document."""


class IngestState(Enum):
    PENDING = "pending"
    """Document is pending ingestion."""

    INGESTED = "ingested"
    """Document has been ingested."""

    FAILED = "failed"
    """Document failed to be ingested. See `ingest_errors` for details."""


class Document(BaseModel):
    """Model for documents in Dewy."""

    id: Optional[int] = None
    collection_id: int

    extracted_text: Optional[str] = None
    """The text that was extracted for this document.

    This is only returned when getting a specific document, not listing documents.

    Will not be set until after the document is ingested.
    """

    url: str

    ingest_state: Optional[IngestState] = None
    ingest_error: Optional[str] = None


class DocumentStatus(BaseModel):
    """Model for document status."""

    id: int
    ingest_state: IngestState
    ingest_error: Optional[str] = None

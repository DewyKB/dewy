from typing import Optional, Sequence

from pydantic import BaseModel

from app.common.models import Chunk

class RetrievedDocument(BaseModel):
    chunks: Sequence[Chunk]
    """Retrieved chunks in the given document.."""

class RetrieveResponse(BaseModel):
    """The response from a chunk retrieval request."""

    synthesized_text: Optional[str]
    """Synthesized text across all documents, if requested."""

    documents: Sequence[RetrievedDocument]
    """Retrieved documents."""
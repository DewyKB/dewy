from typing import Optional, Sequence

from pydantic import BaseModel

from app.common.models import Chunk


class RetrieveResponse(BaseModel):
    """The response from a chunk retrieval request."""

    synthesized_text: Optional[str]
    """Synthesized text across all chunks, if requested."""

    chunks: Sequence[Chunk]
    """Retrieved chunks."""

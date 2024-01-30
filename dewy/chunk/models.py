from typing import Annotated, Literal, Optional, Sequence, Union

from pydantic import BaseModel, Field


class TextChunk(BaseModel):
    id: int
    document_id: int
    kind: Literal["text"] = "text"
    text: str

    raw: bool
    text: str
    start_char_idx: Optional[int] = Field(
        default=None, description="Start char index of the chunk."
    )
    end_char_idx: Optional[int] = Field(
        default=None, description="End char index of the chunk."
    )


class ImageChunk(BaseModel):
    id: int
    document_id: int
    kind: Literal["image"] = "image"

    image: Optional[str] = Field(..., description="Image of the node.")
    image_mimetype: Optional[str] = Field(..., description="Mimetype of the image.")
    image_path: Optional[str] = Field(..., description="Path of the image.")
    image_url: Optional[str] = Field(..., description="URL of the image.")


Chunk = Annotated[Union[TextChunk, ImageChunk], Field(discriminator="kind")]


class RetrieveRequest(BaseModel):
    """A request for retrieving chunks from a collection."""

    collection_id: int
    """The collection to retrieve chunks from."""

    query: str
    """The query string to use for retrieval."""

    n: int = 10
    """The number of chunks to retrieve."""

    # TODO: We may want an option which only excludes nodes included in the summary.
    # For instance -- if we summarize the text statements, maybe it only includes
    # images and tables in the response. But for now, this is a big switch to
    # exclude statements entirely.
    include_text_chunks: bool = True
    """Whether to include text chunks in the result.

    If this is false, no text chunks will be included in the result, although
    the summary (if enbaled) may include information from the chunks.
    """

    include_image_chunks: bool = True
    """Whether to include image chunks in the result.

    If this is false, no image chunks will be included in the result, although
    the summary (if enbaled) may include information from the chunks.
    """

    include_summary: bool = False
    """Whether to include a generated summary."""


class TextResult(BaseModel):
    chunk_id: int
    """The ID of the chunk associated with this result"""

    document_id: int
    """The ID of the document associated with this result"""

    score: float
    """The similarity score of this result."""

    text: str
    "Textual description of the chunk."

    raw: bool
    start_char_idx: Optional[int] = Field(
        default=None, description="Start char index of the chunk."
    )
    end_char_idx: Optional[int] = Field(
        default=None, description="End char index of the chunk."
    )


class ImageResult(BaseModel):
    chunk_id: int
    """The ID of the chunk associated with this result"""

    document_id: int
    """The ID of the document associated with this result"""

    score: float
    """The similarity score of this result."""

    image: Optional[str] = Field(..., description="Image of the node.")
    image_mimetype: Optional[str] = Field(..., description="Mimetype of the image.")
    image_path: Optional[str] = Field(..., description="Path of the image.")
    image_url: Optional[str] = Field(..., description="URL of the image.")


class RetrieveResponse(BaseModel):
    """The response from a retrieval request."""

    summary: Optional[str]
    """Summary of the retrieved chunks."""

    text_results: Sequence[TextResult]
    """Retrieved text chunks."""

    image_results: Sequence[ImageResult]
    """Retrieved image chunks."""

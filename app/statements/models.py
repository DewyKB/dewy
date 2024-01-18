from typing import Literal, Optional, Sequence, Union

from pydantic import BaseModel, Field


class RetrieveRequest(BaseModel):
    """A request for retrieving unstructured (document) results."""

    query: str
    """The query string to use for retrieval."""

    n: int = 10
    """The number of chunks to retrieve."""

    # TODO: We may want an option which only excludes nodes included in the summary.
    # For instance -- if we summarize the text statements, maybe it only includes
    # images and tables in the response. But for now, this is a big switch to
    # exclude statements entirely.
    include_statements: bool = True
    """Whether to include statements in the result.

    If this is false, no statements will be included in the result, although
    the summary (if enbaled) may include information from the statements.
    """

    include_summary: bool = False
    """Whether to include a generated summary."""


class BaseStatement(BaseModel):
    kind: Literal["text", "raw_text", "image"]

    score: Optional[float] = None
    """The similarity score of this statement."""


class TextStatement(BaseStatement):
    kind: Literal["text"] = "text"
    raw: bool
    text: str = Field(default="", description="Text content of the node.")
    start_char_idx: Optional[int] = Field(
        default=None, description="Start char index of the node."
    )
    end_char_idx: Optional[int] = Field(
        default=None, description="End char index of the node."
    )


class ImageStatement(BaseStatement):
    kind: Literal["image"] = "image"
    text: Optional[str] = Field(..., description="Textual description of the image.")
    image: Optional[str] = Field(..., description="Image of the node.")
    image_mimetype: Optional[str] = Field(..., description="Mimetype of the image.")
    image_path: Optional[str] = Field(..., description="Path of the image.")
    image_url: Optional[str] = Field(..., description="URL of the image.")


class RetrieveResponse(BaseModel):
    """The response from a chunk retrieval request."""

    summary: Optional[str]
    """Summary of the retrieved statements."""

    statements: Sequence[Union[TextStatement, ImageStatement]]
    """Retrieved statements."""

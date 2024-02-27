from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationInfo, field_validator

from dewy.common.embeddings import EMBEDDINGS


class DistanceMetric(Enum):
    cosine = "cosine"
    inner_product = "ip"
    l2 = "l2"

    def vector_ops(self) -> str:
        match self:
            case DistanceMetric.cosine:
                return "vector_cosine_ops"
            case DistanceMetric.inner_product:
                return "vector_ip_ops"
            case DistanceMetric.l2:
                return "vector_l2_ops"

    def order_by(self, haystack: str, needle: str) -> str:
        match self:
            case DistanceMetric.cosine:
                return f"{haystack} <=> {needle}"
            case DistanceMetric.inner_product:
                return f"{haystack} <#> {needle}"
            case DistanceMetric.l2:
                return f"{haystack} <-> {needle}"

    def distance(self, haystack: str, needle: str) -> str:
        match self:
            case DistanceMetric.cosine:
                return f"1 - ({haystack} <=> {needle})"
            case DistanceMetric.inner_product:
                return f"({haystack} <#> {needle}) * -1"
            case DistanceMetric.l2:
                return f"{haystack} <-> {needle}"


class Collection(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    """A collection of indexed documents."""

    name: str
    """The name of the collection."""

    text_embedding_model: str
    """The name of the embedding model.

    NOTE: Changing embedding models is not currently supported.
    """

    text_distance_metric: DistanceMetric = DistanceMetric.cosine
    """The distance metric to use on the text embedding.

    NOTE: Changing distance metrics is not currently supported."""


collection_validator = TypeAdapter(Collection)


class CollectionCreate(BaseModel):
    """The request to create a collection."""

    name: str = Field(examples=["my_collection"])
    """The name of the collection."""

    text_embedding_model: str = Field(
        "openai:text-embedding-ada-002",
        examples=["openai:text-embedding-ada-002", "hf:BAAI/bge-small-en"],
    )
    """The name of the embedding model.

    NOTE: Changing embedding models is not currently supported.
    """

    @field_validator("text_embedding_model")
    @classmethod
    def supported_text_embedding_model(cls, v: str, info: ValidationInfo):
        assert (
            v in EMBEDDINGS
        ), f"{info.field_name} must be one of [{', '.join(EMBEDDINGS.keys())}]"
        return v

    text_distance_metric: DistanceMetric = DistanceMetric.cosine
    """The distance metric to use on the text embedding.

    NOTE: Changing distance metrics is not currently supported."""

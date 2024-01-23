<<<<<<< HEAD
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter


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


class Collection(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    """A collection of indexed documents."""
    id: int
    """The ID of the collection."""

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

    text_embedding_model: str = Field(examples=["openai:text-embedding-ada-002", "hf:BAAI/bge-small-en"])
    """The name of the embedding model.

    NOTE: Changing embedding models is not currently supported.
    """

    text_distance_metric: DistanceMetric = DistanceMetric.cosine
    """The distance metric to use on the text embedding.

    NOTE: Changing distance metrics is not currently supported."""

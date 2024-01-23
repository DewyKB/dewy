from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel, ConfigDict, TypeAdapter


@dataclass
class EmbeddingDataMixin:
    dimensions: int


class EmbeddingModel(EmbeddingDataMixin, Enum):
    openai_text_embedding_ada_002 = 1536
    hf_baai_bge_small_en = 384


class Collection(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    """A collection of indexed documents."""
    id: int
    """The ID of the collection."""

    name: str
    """The name of the collection."""


collection_validator = TypeAdapter(Collection)


class CollectionCreate(BaseModel):
    """The request to create a collection."""

    name: str
    """The name of the collection."""


from pydantic import BaseModel, ConfigDict, TypeAdapter

class Collection(BaseModel):
    model_config=ConfigDict(from_attributes=True)

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
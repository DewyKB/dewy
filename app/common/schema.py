from typing import Annotated, Optional

from fastapi import Depends, Request
from sqlalchemy import Engine, UniqueConstraint
from sqlmodel import Field, SQLModel


class Collection(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # TODO: We may want this to be unique per-tenant rather than globally unique names.
    name: str = Field(index=True, unique=True)


class Document(SQLModel, table=True):
    """Schema for documents in the SQL DB."""

    __table_args__ = (
        UniqueConstraint("collection_id", "url"),
        UniqueConstraint("collection_id", "doc_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    collection_id: int = Field(foreign_key="collection.id")

    url: str = Field(index=True)
    doc_id: Optional[str] = Field(default=None)


def _db(request: Request) -> Engine:
    return request.state.engine


DbDep = Annotated[Engine, Depends(_db)]

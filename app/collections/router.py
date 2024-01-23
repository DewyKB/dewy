from typing import Annotated, List

from fastapi import APIRouter, Path

from app.collections.models import Collection, CollectionCreate
from app.common.db import PgConnectionDep

router = APIRouter(prefix="/collections")


@router.put("/")
async def add_collection(
    conn: PgConnectionDep, collection: CollectionCreate
) -> Collection:
    """Create a collection."""
    result = await conn.fetchrow(
        """
        INSERT INTO collection (name) VALUES ($1)
        RETURNING id, name
    """,
        collection.name,
    )
    return Collection.model_validate(dict(result))


@router.get("/")
async def list_collections(conn: PgConnectionDep) -> List[Collection]:
    """List collections."""
    results = await conn.fetch("SELECT id, name FROM collection")
    return [Collection.model_validate(dict(result)) for result in results]


PathCollectionId = Annotated[int, Path(..., description="The collection ID.")]


@router.get("/{id}")
async def get_collection(id: PathCollectionId, conn: PgConnectionDep) -> Collection:
    """Get a specific collection."""
    result = await conn.fetchrow("SELECT id, name FROM collection WHERE id = $1", id)
    return Collection.model_validate(dict(result))

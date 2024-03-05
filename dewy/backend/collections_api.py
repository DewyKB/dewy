from typing import Annotated, List

from fastapi import APIRouter, Path, Response, status

from dewy.domain import collection

from ._dependencies import PgConnectionDep

router = APIRouter(prefix="/collections")


@router.post("/")
async def add_collection(
    conn: PgConnectionDep, request: collection.Collection
) -> collection.Collection:
    """Create a collection."""
    return await collection.create_collection(conn, request)


@router.get("/")
async def list_collections(
    conn: PgConnectionDep,
) -> List[collection.Collection]:
    """List collections."""
    return await collection.list_collections(conn)


@router.get("/{name}")
async def get_collection(
    name: Annotated[str, Path(..., description="The collection name.")], conn: PgConnectionDep
) -> collection.Collection:
    """Get a specific collection."""
    return await collection.get_collection(conn, name)


@router.delete("/{name}")
async def delete_collection(
    conn: PgConnectionDep, name: Annotated[str, Path(..., description="The collection name.")]
) -> collection.Collection:
    """Delete a collection and all documents contained within it."""
    await collection.delete_collection(conn, name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from typing import Annotated, List
from fastapi import APIRouter, Path
from sqlmodel import Session, select

from app.common.schema import Collection, DbDep

router = APIRouter(tags=["collections"], prefix="/collections")

@router.put("/")
async def add(db: DbDep, collection: Collection) -> Collection:
    """Create a collection."""
    with Session(db) as session:
        session.add(collection)
        session.commit()
        session.refresh(collection)
        return collection

@router.get("/")
async def list(db: DbDep) -> List[Collection]:
    """List collections."""
    with Session(db) as session:
        collections = session.exec(select(Collection)).all()
        return collections

PathCollectionId = Annotated[int, Path(..., description="The collection ID.")]

@router.get("/{id}")
async def get(id: PathCollectionId, db: DbDep) -> Collection:
    """Get a specific collection."""
    with Session(db) as session:
        return session.get(Collection, id)
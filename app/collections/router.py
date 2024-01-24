from typing import Annotated, List

from fastapi import APIRouter, Path

from app.collections.models import Collection, CollectionCreate
from app.common.db import PgConnectionDep

router = APIRouter(prefix="/collections")


def get_dimensions(model: str) -> int:
    # TODO: Consider instantiating the model and applying it to a string
    # to determine the dimensions. This would make it easier to support
    # new models.
    match model:
        case "openai:text-embedding-ada-002":
            return 1536
        case "hf:BAAI/bge-small-en":
            return 384
        case _:
            raise ValueError(f"Unsupported model '{model}'")


@router.put("/")
async def add_collection(
    conn: PgConnectionDep, collection: CollectionCreate
) -> Collection:
    """Create a collection."""
    dimensions = get_dimensions(collection.text_embedding_model)
    async with conn.transaction():
        result = await conn.fetchrow(
            """
            INSERT INTO collection (name, text_embedding_model, text_distance_metric)
            VALUES ($1, $2, $3)
            RETURNING id, name, text_embedding_model, text_distance_metric
        """,
            collection.name,
            collection.text_embedding_model,
            collection.text_distance_metric.value,
        )

        # Create a separate *partial* index on each collection.
        # This allows us to define different dimensions (and vector distance) for
        # each collection.
        #
        # https://github.com/pgvector/pgvector?tab=readme-ov-file#can-i-store-vectors-with-different-dimensions-in-the-same-column
        id = result["id"]
        vector_ops = collection.text_distance_metric.vector_ops()
        await conn.execute(
            f"""
            CREATE INDEX embedding_collection_{id}_index
            ON embedding
            USING hnsw ((embedding::vector({dimensions})) {vector_ops})
            WHERE collection_id = {id}
            """
        )
    return Collection.model_validate(dict(result))


@router.get("/")
async def list_collections(conn: PgConnectionDep) -> List[Collection]:
    """List collections."""
    results = await conn.fetch("SELECT id, name, text_embedding_model FROM collection")
    return [Collection.model_validate(dict(result)) for result in results]


PathCollectionId = Annotated[int, Path(..., description="The collection ID.")]


@router.get("/{id}")
async def get_collection(id: PathCollectionId, conn: PgConnectionDep) -> Collection:
    """Get a specific collection."""
    result = await conn.fetchrow(
        """
        SELECT id, name, text_embedding_model
        FROM collection
        WHERE id = $1
        """,
        id,
    )
    return Collection.model_validate(dict(result))

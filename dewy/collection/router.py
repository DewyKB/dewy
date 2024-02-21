from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Path, status, Response
from loguru import logger

from dewy.collection.models import Collection, CollectionCreate
from dewy.common.collection_embeddings import get_dimensions
from dewy.common.db import PgConnectionDep, PgPoolDep

router = APIRouter(prefix="/collections")


@router.post("/")
async def add_collection(conn: PgConnectionDep, collection: CollectionCreate) -> Collection:
    """Create a collection."""
    dimensions = await get_dimensions(conn, collection.text_embedding_model)
    logger.info("Dimensions: {}", dimensions)
    async with conn.transaction():
        result = await conn.fetchrow(
            """
            INSERT INTO collection (
                name,
                text_embedding_model,
                text_distance_metric
            ) VALUES ($1, $2, $3)
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
async def list_collections(
    conn: PgConnectionDep,
) -> List[Collection]:
    """List collections."""
    results = await conn.fetch(
        """
        SELECT name, text_embedding_model
        FROM collection
        """,
    )
    return [Collection.model_validate(dict(result)) for result in results]


PathCollection = Annotated[str, Path(..., description="The collection name.")]


@router.get("/{name}")
async def get_collection(name: PathCollection, conn: PgConnectionDep) -> Collection:
    """Get a specific collection."""
    result = await conn.fetchrow(
        """
        SELECT name, text_embedding_model
        FROM collection
        WHERE lower(name) = lower($1)
        """,
        name,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No collection named '{name}'"
        )

    return Collection.model_validate(dict(result))

@router.delete("/{name}")
async def delete_collection(pg_pool: PgPoolDep, name: PathCollection) -> Collection:
    """Delete a collection and all documents contained within it."""
    async with pg_pool.acquire() as conn:
        async with conn.transaction():
            collection_id = await conn.fetchval(
                """
                SELECT id
                FROM collection
                WHERE name = $1
                """,
                name,
            )

            if not collection_id:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"No collection with name {name}"
            )

            # Delete any embeddings
            await conn.execute(
                """
                DELETE FROM embedding e
                WHERE collection_id = $1
                """,
                collection_id,
            )
            # Delete any chunks
            await conn.execute(
                """
                DELETE from chunk c
                USING document d
                WHERE c.document_id = d.id
                AND d.collection_id = $1
                """,
                collection_id,
            )
            # Delete any documents
            await conn.execute(
                """
                DELETE from document
                WHERE collection_id = $1
                """,
                collection_id,
            )
            # Delete the collection
            await conn.execute(
                """
                DELETE from collection
                WHERE id = $1
                """,
                collection_id,
            )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

from __future__ import annotations

import dataclasses
from enum import Enum
from typing import List

import asyncpg
import pydantic

from dewy.domain.embedding_models import EMBEDDINGS

from ._errors import NoSuchCollection


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


class Collection(pydantic.BaseModel):
    """A collection of indexed documents."""

    name: str = pydantic.Field(examples=["my_collection"])
    """The name of the collection."""

    text_embedding_model: str = pydantic.Field(
        "openai:text-embedding-ada-002",
        examples=["openai:text-embedding-ada-002", "hf:BAAI/bge-small-en"],
    )
    """The name of the embedding model.

    NOTE: Changing embedding models is not currently supported.
    """

    text_distance_metric: DistanceMetric = DistanceMetric.cosine
    """The distance metric to use on the text embedding.

    NOTE: Changing distance metrics is not currently supported."""

    @pydantic.field_validator("text_embedding_model")
    @classmethod
    def supported_text_embedding_model(cls, v: str, info: pydantic.ValidationInfo):
        assert (
            v in EMBEDDINGS
        ), f"{info.field_name} must be one of [{', '.join(EMBEDDINGS.keys())}]"
        return v


@dataclasses.dataclass
class CollectionConfig:
    """Information about a collection."""

    collection_id: int
    """The ID of the collection."""

    text_embedding_model: str
    """The name of the embedding model to use."""

    text_distance_metric: DistanceMetric
    """The name of the distance metric to use."""

    extract_tables: bool = False
    """Whether tables should be extracted."""

    extract_images: bool = False
    """Whether images should be extracted."""

    @staticmethod
    async def for_collection(conn: asyncpg.Connection, collection: str) -> CollectionConfig:
        result = await conn.fetchrow(
            """
            SELECT
                id,
                text_embedding_model,
                text_distance_metric
            FROM collection
            WHERE lower(name) = lower($1);
            """,
            collection,
        )

        return CollectionConfig(
            collection_id=result["id"],
            text_embedding_model=result["text_embedding_model"],
            text_distance_metric=DistanceMetric(result["text_distance_metric"]),
        )

    @staticmethod
    async def for_document_id(conn: asyncpg.Connection, document_id: int) -> CollectionConfig:
        """Retrieve the collection embeddings and the URL of the given document."""

        result = await conn.fetchrow(
            """
            SELECT
                c.id as collection_id,
                c.text_embedding_model,
                c.text_distance_metric
            FROM document d
            JOIN collection c ON d.collection_id = c.id
            WHERE d.id = $1;
            """,
            document_id,
        )

        return CollectionConfig(
            collection_id=result["collection_id"],
            text_embedding_model=result["text_embedding_model"],
            text_distance_metric=DistanceMetric(result["text_distance_metric"]),
        )


def _collection_from_record(row: asyncpg.Record) -> Collection:
    return Collection(
        name=row["name"],
        text_embedding_model=row["text_embedding_model"],
        text_distance_metric=row["text_distance_metric"],
    )


async def create_collection(conn: asyncpg.Connection, collection: Collection) -> Collection:
    dimensions = EMBEDDINGS[collection.text_embedding_model].dimensions

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

        return _collection_from_record(result)


async def list_collections(conn: asyncpg.Connection) -> List[Collection]:
    results = await conn.fetch(
        """
        SELECT name, text_embedding_model, text_distance_metric
        FROM collection
        """,
    )
    return [_collection_from_record(row) for row in results]


async def get_collection(conn: asyncpg.Collection, name: str) -> Collection:
    result = await conn.fetchrow(
        """
        SELECT name, text_embedding_model, text_distance_metric
        FROM collection
        WHERE lower(name) = lower($1)
        """,
        name,
    )

    if not result:
        raise NoSuchCollection(name)

    return _collection_from_record(result)


async def delete_collection(conn: asyncpg.Collection, name: str):
    id = await conn.fetchval(
        """
        DELETE from collection
        WHERE name = $1
        RETURNING id
        """,
        name,
    )
    if not id:
        raise NoSuchCollection(name)

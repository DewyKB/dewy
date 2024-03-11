from functools import lru_cache
from typing import List, Literal, Optional, Sequence, Tuple, Union, overload

import asyncpg
from pydantic import BaseModel, Field

from dewy.config import ServeConfig
from dewy.domain._errors import NoSuchChunk
from dewy.domain.collection import CollectionConfig, DistanceMetric
from dewy.domain.embedding_models import EMBEDDINGS, text_embedding_model


@overload
def _encode_chunk(c: str) -> str: ...
@overload
def _encode_chunk(c: None) -> None: ...


def _encode_chunk(c: Optional[str]) -> Optional[str]:
    if c is None:
        return None

    # We believe that either invalid unicode or the occurrence
    # of nulls was causing problems that *looked* like only the
    # first page from a PDF was being indexed
    # (https://github.com/DewyKB/dewy/issues/20). We do not know
    # that all of this is truly necessary.
    encoded = c.encode("utf-8").decode("utf-8", "ignore")
    return encoded.replace("\x00", "\ufffd")


async def insert_text_chunks(
    conn: asyncpg.Connection, document_id: int, chunks: List[str]
) -> List[Tuple[int, str]]:
    """Insert the chunks associated with the given docuemnt.

    NOTE: This does not insert corresponding embeddings for the chunks.

    Returns:
    The IDs and content of each inserted chunk.
    """

    # Make sure we deleted chunks earlier.
    # TODO: Introduce document versions / ingestions / iterations so
    # we can do this search as "chunks associated with this version"?
    assert (
        await conn.fetchval("SELECT COUNT(*) FROM chunk WHERE document_id = $1", document_id) == 0
    )

    await conn.executemany(
        """
        INSERT INTO chunk (document_id, kind, text)
        VALUES ($1, $2, $3);
        """,
        [(document_id, "text", _encode_chunk(text)) for text in chunks],
    )

    chunks = await conn.fetch("SELECT id, text FROM chunk WHERE document_id = $1", document_id)

    return [(chunk["id"], chunk["text"]) for chunk in chunks]


class TextChunk(BaseModel):
    kind: Literal["text"] = "text"

    id: int
    """The ID of the chunk associated with this result"""

    document_id: int
    """The ID of the document associated with this result"""

    score: Optional[float] = None
    """The similarity score of this result."""

    text: str
    "Textual description of the chunk."

    raw: bool
    start_char_idx: Optional[int] = Field(
        default=None, description="Start char index of the chunk."
    )
    end_char_idx: Optional[int] = Field(default=None, description="End char index of the chunk.")


class ImageChunk(BaseModel):
    id: int
    document_id: int
    kind: Literal["image"] = "image"

    image: Optional[str] = Field(..., description="Image of the node.")
    image_mimetype: Optional[str] = Field(..., description="Mimetype of the image.")
    image_path: Optional[str] = Field(..., description="Path of the image.")
    image_url: Optional[str] = Field(..., description="URL of the image.")


class RetrievedChunks(BaseModel):
    """The response from a retrieval request."""

    summary: Optional[str] = None
    """Summary of the retrieved chunks."""

    text_chunks: Sequence[TextChunk] = []
    """Retrieved text chunks."""

    image_chunks: Sequence[ImageChunk] = []
    """Retrieved image chunks."""


@lru_cache
def _chunk_retrieval_query(
    dimensions: int,
    distance_metric: DistanceMetric,
) -> str:
    """Compute the retrieval query.

    We intentionally leave "holes" for the actual query, dimensions, and document ID filters.

    Returns:
    A SQL query string with the following template variables:
    - collection_id
    - embedded query string
    - offset (first chunk to return)
    - limit (number of chunks to return)
    - document_ids to filter to
    """

    field = f"embedding::vector({dimensions})"
    return f"""
        WITH relevant_embeddings AS (
            SELECT
                chunk_id,
                {distance_metric.distance(field, "$2")} AS score
            FROM embedding
            WHERE collection_id = $1
            ORDER BY {distance_metric.order_by(field, "$2")}
        )
        SELECT
            relevant_embeddings.chunk_id AS id,
            chunk.text AS text,
            relevant_embeddings.score AS score,
            chunk.document_id AS document_id
        FROM relevant_embeddings
        JOIN chunk
        ON chunk.id = relevant_embeddings.chunk_id
        WHERE (CAST($5 AS integer[]) IS NULL OR chunk.document_id = ANY($5))
        OFFSET $3
        LIMIT $4
    """


def _text_chunk_from_record(row: asyncpg.Record) -> TextChunk:
    return TextChunk(
        id=row["id"],
        document_id=row["document_id"],
        score=row.get("score"),
        text=row["text"],
        raw=True,
        start_char_idx=None,
        end_char_idx=None,
    )


async def retrieve_chunks(
    conn: asyncpg.Connection,
    config: ServeConfig,
    collection: str,
    query: str,
    offset: int = 0,
    limit: int = 10,
    document_ids: Optional[List[int]] = None,
    include_text_chunks: bool = True,
) -> RetrievedChunks:
    """
    Retrieve the chunks nearest to the query string.
    """

    text_chunks = []
    if include_text_chunks:
        collection_config = await CollectionConfig.for_collection(conn, collection)

        sql_query = _chunk_retrieval_query(
            dimensions=EMBEDDINGS[collection_config.text_embedding_model].dimensions,
            distance_metric=collection_config.text_distance_metric,
        )

        embedded_query = await text_embedding_model(
            collection_config.text_embedding_model,
            config,
        ).aembed_query(query)

        rows = await conn.fetch(
            sql_query,
            collection_config.collection_id,
            embedded_query,
            offset,
            limit,
            document_ids,
        )

        text_chunks = [_text_chunk_from_record(row) for row in rows]

    return RetrievedChunks(text_chunks=text_chunks)


async def list_chunks(
    conn: asyncpg.Connection,
    collection: Optional[str] = None,
    offset: int = 0,
    limit: int = 10,
    document_ids: Optional[List[int]] = None,
) -> List[Union[TextChunk, ImageChunk]]:
    """
    List chunks.
    """
    results = await conn.fetch(
        """
        SELECT k.id, k.document_id, k.kind, TRUE as raw, k.text
        FROM chunk k
        JOIN document d ON d.id = k.document_id
        JOIN collection c ON d.collection_id = c.id
        WHERE (CAST($2 AS integer[]) IS NULL OR k.document_id = ANY($2))
        AND lower(c.name) = coalesce(lower($1), lower(c.name))
        ORDER BY k.id
        OFFSET $3
        LIMIT $4
        """,
        collection,
        document_ids,
        offset,
        limit,
    )

    text_chunks = [_text_chunk_from_record(row) for row in results]
    return text_chunks


async def remove_chunks_for_document(
    conn: asyncpg.Connection,
    document_id: int,
):
    # Delete the chunks. The embeddings will be deleted by a cascade.
    await conn.execute(
        """
        DELETE FROM chunk
        WHERE document_id = $1
        """,
        document_id,
    )


async def get_chunk(
    conn: asyncpg.Connection,
    chunk_id: int,
) -> Union[TextChunk, ImageChunk]:
    result = await conn.fetchrow(
        """
        SELECT id, document_id, kind, text
        FROM chunk WHERE id = $1
        """,
        id,
    )

    if result is None:
        raise NoSuchChunk(chunk_id)
    return _text_chunk_from_record(result)

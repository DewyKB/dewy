from dataclasses import dataclass
from typing import List

import asyncpg


@dataclass
class TextEmbedding:
    chunk_id: int
    text: str
    embedding: List[float]


async def insert_embeddings(
    conn: asyncpg.Connection,
    collection_id: int,
    embeddings: List[TextEmbedding],
):
    await conn.executemany(
        """
        INSERT INTO embedding (collection_id, chunk_id, key_text, embedding)
        VALUES ($1, $2, $3, $4);
        """,
        [(collection_id, e.chunk_id, e.text, e.embedding) for e in embeddings],
    )

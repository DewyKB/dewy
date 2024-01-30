from typing import List, Self, Tuple

import asyncpg
from llama_index.embeddings import BaseEmbedding
from llama_index.node_parser import SentenceSplitter
from llama_index.schema import TextNode
from loguru import logger

from dewy.chunk.models import TextResult
from dewy.collection.models import DistanceMetric
from dewy.config import settings

from .extract import extract


class CollectionEmbeddings:
    """Helper class for working with the embeddings in a collection."""

    def __init__(
        self,
        pg_pool: asyncpg.Pool,
        *,
        collection_id: int,
        text_embedding_model: str,
        text_embedding_dimensions: int,
        text_distance_metric: DistanceMetric,
    ) -> None:
        """Create a new CollectionEmbeddings."""
        self._pg_pool = pg_pool
        self.collection_id = collection_id
        self.text_embedding_model = text_embedding_model
        self.text_distance_metric = text_distance_metric

        self.extract_tables = False
        self.extract_images = False

        # TODO: Look at a sentence window splitter?
        self._splitter = SentenceSplitter()
        self._embedding = _resolve_embedding_model(self.text_embedding_model)

        field = f"embedding::vector({text_embedding_dimensions})"

        # TODO: Figure out how to limit by the number of *chunks* not the number
        # of embeddings.
        self._retrieve_embeddings = f"""
        SELECT
          chunk_id,
          {self.text_distance_metric.distance(field, "$2")} AS score
        FROM embedding
        WHERE collection_id = $1
        ORDER BY {self.text_distance_metric.order_by(field, "$2")}
        LIMIT $3
        """

        self._retrieve_chunks = f"""
        WITH relevant_embeddings AS (
          SELECT
            chunk_id,
            {self.text_distance_metric.distance(field, "$2")} AS score
          FROM embedding
          WHERE collection_id = $1
          ORDER BY {self.text_distance_metric.order_by(field, "$2")}
        )
        SELECT
          relevant_embeddings.chunk_id AS chunk_id,
          chunk.text AS text,
          relevant_embeddings.score AS score,
          chunk.document_id AS document_id
        FROM relevant_embeddings
        JOIN chunk
        ON chunk.id = relevant_embeddings.chunk_id
        LIMIT $3
        """

    @staticmethod
    async def for_collection_id(pg_pool: asyncpg.Pool, collection_id: int) -> Self:
        """Retrieve the collection embeddings of the given collection."""
        async with pg_pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                SELECT
                    collection.id as id,
                    text_embedding_model,
                    text_distance_metric,
                    text_embedding_dimensions.dimensions AS text_embedding_dimensions
                FROM collection
                JOIN text_embedding_dimensions
                    ON text_embedding_dimensions.name = collection.text_embedding_model
                WHERE collection.id = $1;
                """,
                collection_id,
            )

            return CollectionEmbeddings(
                pg_pool,
                collection_id=result["id"],
                text_embedding_model=result["text_embedding_model"],
                text_embedding_dimensions=result["text_embedding_dimensions"],
                text_distance_metric=DistanceMetric(result["text_distance_metric"]),
            )

    @staticmethod
    async def for_document_id(pg_pool: asyncpg.Pool, document_id: int) -> (str, Self):
        """Retrieve the collection embeddings and the URL of the given document."""

        # TODO: Ideally the collection embeddings would be cached, and this
        # wouldn't need to exist.
        async with pg_pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                SELECT
                    document.url as url,
                    collection.name,
                    collection.id as id,
                    collection.text_embedding_model,
                    collection.text_distance_metric,
                    text_embedding_dimensions.dimensions AS text_embedding_dimensions
                FROM document
                JOIN collection ON document.collection_id = collection.id
                JOIN text_embedding_dimensions
                    ON text_embedding_dimensions.name = collection.text_embedding_model
                WHERE document.id = $1;
                """,
                document_id,
            )

            # TODO: Cache the configured ingestions, and only recreate when needed?
            configured_ingestion = CollectionEmbeddings(
                pg_pool,
                collection_id=result["id"],
                text_embedding_model=result["text_embedding_model"],
                text_embedding_dimensions=result["text_embedding_dimensions"],
                text_distance_metric=DistanceMetric(result["text_distance_metric"]),
            )
            return (result["url"], configured_ingestion)

    async def retrieve_text_embeddings(
        self, query: str, n: int = 10
    ) -> List[Tuple[int, float]]:
        """Retrieve embeddings related to the given query.

        Parameters:
        - query: The query to retrieve matching embeddings for.
        - n: The number of embeddings to retrieve.

        Returns:
        List of `(chunk_id, score)` pairs from the embeddings.
        """
        embedded_query = await self._embedding.aget_text_embedding(query)

        async with self._pg_pool.acquire() as conn:
            logger.info("Executing SQL query for chunks from {}", self.collection_id)
            embeddings = await conn.fetch(
                self._retrieve_embeddings, self.collection_id, embedded_query, n
            )
            embeddings = [e["chunk_id"] for e in embeddings]
            return embeddings

    async def retrieve_text_chunks(self, query: str, n: int = 10) -> List[TextResult]:
        """Retrieve embeddings related to the given query.

        Parameters:
        - query: The query to retrieve matching embeddings for.
        - n: The number of embeddings to retrieve.

        Returns:
        List of chunk_ids from the embeddings.
        """
        embedded_query = await self._embedding.aget_text_embedding(query)

        async with self._pg_pool.acquire() as conn:
            logger.info("Executing SQL query for chunks from {}", self.collection_id)
            embeddings = await conn.fetch(
                self._retrieve_chunks, self.collection_id, embedded_query, n
            )
            embeddings = [
                TextResult(
                    chunk_id=e["chunk_id"],
                    document_id=e["document_id"],
                    score=e["score"],
                    text=e["text"],
                    raw=True,
                    start_char_idx=None,
                    end_char_idx=None,
                )
                for e in embeddings
            ]
            return embeddings

    async def ingest(self, document_id: int, url: str) -> None:
        logger.info("Loading content for document {} from '{}'", document_id, url)
        extracted = await extract(
            url, extract_tables=self.extract_tables, extract_images=self.extract_images
        )
        if extracted.is_empty():
            logger.error(
                "No content retrieved from for document {} from '{}'", document_id, url
            )
            return

        logger.info(
            "Chunking text of length {} for {}", len(extracted.text), document_id
        )

        # Extract chunks (snippets) and perform the direct embedding.
        text_chunks = await self._chunk_sentences(extracted.text)

        logger.info("Chunking produced {} chunks for {}", len(text_chunks), document_id)

        # TODO: support non-text chunks
        # TODO: support non-snippet text chunks (eg., summary values)
        # TODO: support indirect embeddings
        async with self._pg_pool.acquire() as conn:
            async with conn.transaction():

                def encode_chunk(c: str) -> str:
                    # We believe that either invalid unicode or the occurrence
                    # of nulls was causing problems that *looked* like only the
                    # first page from a PDF was being indexed
                    # (https://github.com/DewyKB/dewy/issues/20). We do not know
                    # that all of this is truly necessary.
                    encoded = c.encode("utf-8").decode("utf-8", "ignore")
                    return encoded.replace("\x00", "\uFFFD")

                # First, insert the chunks.
                await conn.executemany(
                    """
                    INSERT INTO chunk (document_id, kind, text)
                    VALUES ($1, $2, $3);
                    """,
                    [
                        (document_id, "text", encode_chunk(text_chunk))
                        for text_chunk in text_chunks
                    ],
                )

                # Then, embed each of those chunks.
                # We assume no chunks for the document existed before, so we can iterate
                # over the chunks.
                chunks = conn.cursor(
                    "SELECT id, text FROM chunk WHERE document_id = $1", document_id
                )

                # TODO: Write this loop in a cleaner async way, to limit the number of
                # in-flight requests as well as batching up the embedding requests.
                # Currently, this uses Llama Index embeddings, which requires we put
                # all the texts to embed in a list.
                #
                # Ideally, we could take a chunk of embeddings, embed them, and then
                # start writing that to the DB asynchronously.
                embedding_chunks = [
                    (chunk["id"], chunk["text"]) async for chunk in chunks
                ]

                # Extract just the text and embed it.
                logger.info(
                    "Computing {} embeddings for {}", len(embedding_chunks), document_id
                )
                embeddings = await self._embedding.aget_text_embedding_batch(
                    [item[1] for item in embedding_chunks]
                )

                # Change the shape to a list of triples (for writing to the DB)
                embeddings = [
                    (self.collection_id, chunk_id, chunk_text, embedding)
                    for (chunk_id, chunk_text), embedding in zip(
                        embedding_chunks, embeddings
                    )
                ]

                logger.info(
                    "Writing {} embeddings for {}", len(embeddings), document_id
                )
                await conn.executemany(
                    """
                    INSERT INTO embedding (collection_id, chunk_id, key_text, embedding)
                    VALUES ($1, $2, $3, $4)
                    """,
                    embeddings,
                )
                logger.info("Wrote {} embeddings for {}", len(embeddings), document_id)

                await conn.execute(
                    """
                    UPDATE document
                    SET ingest_state = 'ingested', ingest_error = NULL
                    WHERE id = $1
                    """,
                    document_id,
                )

    async def _chunk_sentences(self, text: str) -> List[str]:
        # This uses llama index a bit oddly. Unfortunately:
        #  - It returns `BaseNode` even though we know these are `TextNode`
        #  - It returns a `List` rather than an `Iterator` / `Generator`, so
        #    all resulting nodes are resident in memory.
        #  - It uses metadata to return the "window" (if using sentence windows).
        return [node.text for node in await self._splitter.acall([TextNode(text=text)])]


DEFAULT_OPENAI_EMBEDDING_MODEL: str = "openai:text-embedding-ada-002"
DEFAULT_HF_EMBEDDING_MODEL: str = "hf:BAAI/bge-small-en"


async def get_dimensions(conn: asyncpg.Connection, model_name: str) -> int:
    dimensions = await conn.fetchval(
        """
        SELECT dimensions
        FROM text_embedding_dimensions
        WHERE name = $1
        """,
        model_name,
    )

    if dimensions is not None:
        return dimensions

    model = _resolve_embedding_model(model_name)
    dimensions = len(await model.aget_text_embedding("test string"))

    # TODO: Deal with concurrency? I suspect it is OK if this fails
    # due to the uniqueness constraint, and we should just move on.
    # Someone wrote the value for that name to the table, and we should
    # have determined the same values.
    await conn.execute(
        """
        INSERT INTO text_embedding_dimensions (name, dimensions)
        VALUES ($1, $2)
        """,
        model_name,
        dimensions,
    )

    return dimensions


def _resolve_embedding_model(model: str) -> BaseEmbedding:
    if not model:
        if settings.OPENAI_API_KEY:
            model = DEFAULT_OPENAI_EMBEDDING_MODEL
        else:
            model = DEFAULT_HF_EMBEDDING_MODEL

    split = model.split(":", 2)
    if split[0] == "openai":
        from llama_index.embeddings import OpenAIEmbedding

        return OpenAIEmbedding(model=split[1])
    elif split[0] == "hf":
        from llama_index.embeddings import HuggingFaceEmbedding

        return HuggingFaceEmbedding(model_name=split[1])
    else:
        raise ValueError(f"Unrecognized embedding model '{model}'")

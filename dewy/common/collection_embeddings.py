import dataclasses
from typing import List, Optional, Self, Tuple, Union

import asyncpg
from langchain.text_splitter import RecursiveCharacterTextSplitter
from loguru import logger

from dewy.chunk.models import TextResult
from dewy.collection.models import DistanceMetric
from dewy.common.embeddings import EMBEDDINGS
from dewy.config import Config

from .extract import extract_content, extract_url


@dataclasses.dataclass
class IngestContent:
    filename: Optional[str]
    content_type: Optional[str]
    size: Optional[int]
    content_bytes: bytes = dataclasses.field(repr=False)


@dataclasses.dataclass
class IngestURL:
    url: str


class CollectionEmbeddings:
    """Helper class for working with the embeddings in a collection."""

    def __init__(
        self,
        pg_pool: asyncpg.Pool,
        config: Config,
        *,
        collection_id: int,
        text_embedding_model: str,
        text_distance_metric: DistanceMetric,
    ) -> None:
        """Create a new CollectionEmbeddings."""
        self._pg_pool = pg_pool
        self.collection_id = collection_id
        self.text_embedding_model = text_embedding_model
        self.text_distance_metric = text_distance_metric

        self.extract_tables = False
        self.extract_images = False

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        embedding = EMBEDDINGS[self.text_embedding_model]
        self._embedding = embedding.factory(config)

        field = f"embedding::vector({embedding.dimensions})"

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
    async def for_collection(pg_pool: asyncpg.Pool, config: Config, collection: str) -> Self:
        """Retrieve the collection embeddings of the given collection."""
        async with pg_pool.acquire() as conn:
            result = await conn.fetchrow(
                """
                SELECT
                    c.id as collection_id,
                    c.text_embedding_model,
                    c.text_distance_metric
                FROM collection c
                WHERE lower(c.name) = lower($1);
                """,
                collection,
            )

            return CollectionEmbeddings(
                pg_pool,
                config,
                collection_id=result["collection_id"],
                text_embedding_model=result["text_embedding_model"],
                text_distance_metric=DistanceMetric(result["text_distance_metric"]),
            )

    @staticmethod
    async def for_document_id(pg_pool: asyncpg.Pool, config: Config, document_id: int) -> Self:
        """Retrieve the collection embeddings and the URL of the given document."""

        # TODO: Ideally the collection embeddings would be cached, and this
        # wouldn't need to exist.
        async with pg_pool.acquire() as conn:
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

            # TODO: Cache the configured ingestions, and only recreate when needed?
            configured_ingestion = CollectionEmbeddings(
                pg_pool,
                config,
                collection_id=result["collection_id"],
                text_embedding_model=result["text_embedding_model"],
                text_distance_metric=DistanceMetric(result["text_distance_metric"]),
            )
            return configured_ingestion

    async def retrieve_text_embeddings(self, query: str, n: int = 10) -> List[Tuple[int, float]]:
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
        embedded_query = await self._embedding.aembed_query(query)

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

    async def ingest(self, document_id: int, request: Union[IngestURL, IngestContent]) -> None:
        extracted = None
        if isinstance(request, IngestContent):
            logger.info("Loading content for document {} from content {}", document_id, request)
            extracted = await extract_content(
                request.content_bytes,
                extract_tables=self.extract_tables,
                extract_images=self.extract_images,
            )
        elif isinstance(request, IngestURL):
            logger.info(
                "Loading content for document {} from url '{}'",
                document_id,
                request.url,
            )
            extracted = await extract_url(
                request.url,
                extract_tables=self.extract_tables,
                extract_images=self.extract_images,
            )
        else:
            raise ValueError(f"Ingest expected URL or Content, but was {request}")

        if extracted.is_empty():
            logger.error(
                "No content retrieved from for document {} from '{}'",
                document_id,
                request,
            )
            return

        logger.info("Chunking text of length {} for {}", len(extracted.text), document_id)

        # Extract chunks (snippets) and perform the direct embedding.
        text_chunks = await self._chunk_sentences(extracted.text)

        logger.info("Chunking produced {} chunks for {}", len(text_chunks), document_id)

        # TODO: support non-text chunks
        # TODO: support non-snippet text chunks (eg., summary values)
        # TODO: support indirect embeddings
        async with self._pg_pool.acquire() as conn:
            async with conn.transaction():
                status = await conn.fetchval(
                    "SELECT ingest_state FROM document WHERE id = $1", document_id
                )
                if status != "pending":
                    raise NotImplementedError(
                        "Updating content of ingested document not supported."
                    )

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
                embedding_chunks = [(chunk["id"], chunk["text"]) async for chunk in chunks]

                # Extract just the text and embed it.
                logger.info("Computing {} embeddings for {}", len(embedding_chunks), document_id)
                embeddings = await self._embedding.aembed_documents(
                    [item[1] for item in embedding_chunks]
                )

                # Change the shape to a list of triples (for writing to the DB)
                embeddings = [
                    (self.collection_id, chunk_id, chunk_text, embedding)
                    for (chunk_id, chunk_text), embedding in zip(embedding_chunks, embeddings)
                ]

                logger.info("Writing {} embeddings for {}", len(embeddings), document_id)
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
                    SET
                      ingest_state = 'ingested',
                      ingest_error = NULL,
                      extracted_text = $2
                    WHERE id = $1
                    """,
                    document_id,
                    encode_chunk(extracted.text),
                )
            logger.info("Finished updating embeddings for document {}", document_id)

    async def _chunk_sentences(self, text: str) -> List[str]:
        return self._splitter.split_text(text)

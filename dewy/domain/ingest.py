import base64
import dataclasses
from typing import List, Optional, Tuple, Union

import asyncpg
from loguru import logger

from dewy.common.extract import ExtractResult, extract_content, extract_url
from dewy.config import ServeConfig
from dewy.domain import chunks, documents, embeddings
from dewy.domain.collection import CollectionConfig
from dewy.domain.embedding_models import text_embedding_model


@dataclasses.dataclass
class IngestContent:
    filename: Optional[str]
    """The filename of the content to ingest. Set by the client."""

    content_type: Optional[str]
    """The mimetype of the content. Set by the client."""

    size: Optional[int]
    """The size of the content. Set by the client."""

    content_bytes: bytes = dataclasses.field(repr=False)
    """The actual bytes of the uploaded content to ingest."""


@dataclasses.dataclass
class IngestURL:
    """Dataclass indicating a URL to ingest."""

    url: str
    """The url of the content to ingest."""


async def ingest(
    document_id: int,
    request: Union[IngestContent, IngestURL],
    conn: asyncpg.Connection,
    config: ServeConfig,
) -> None:
    # For testing, we allow the `error://` URL to trigger an ingestion error.
    # This verifies that the method that *calls* this properly catches and reports
    # errors.
    if isinstance(request, IngestURL) and request.url.startswith("error://"):
        raise RuntimeError(request.url.removeprefix("error://"))

    collection_config = await CollectionConfig.for_document_id(conn, document_id)
    extracted = await _extract(request, collection_config=collection_config)

    if not extracted:
        logger.warning("No content retrieved for document {} from '{}'", document_id, request)

        await documents.update_status(
            conn, document_id, documents.IngestState.INGESTED, extracted_text=extracted
        )
        return

    logger.info("Chunking text of length {}", len(extracted.text))
    text_chunks = await _chunk(extracted.text)

    logger.info("Writing chunks and embeddings for {}", document_id)
    async with conn.transaction():
        # Check that the status hasn't been applied.
        status = await documents.get_status(conn, document_id)
        if status != documents.IngestState.PENDING:
            raise NotImplementedError(f"Updating content of document with status {status}")

        # Insert the chunks.
        text_chunks = await chunks.insert_text_chunks(conn, document_id, text_chunks)

        logger.info("Computing embeddings for {} text chunks", len(text_chunks))
        text_embeddings = await _embed_text(
            text_chunks, collection_config=collection_config, config=config
        )

        # Insert computed embeddings.
        await embeddings.insert_embeddings(conn, collection_config.collection_id, text_embeddings)

        # Update the status.
        await documents.update_status(
            conn, document_id,
            documents.IngestState.INGESTED,
            extracted_text = extracted.text
        )

    logger.info("Finished ingesting {} document {}", request, document_id)


async def _extract(
    request: Union[IngestURL, IngestContent], collection_config: CollectionConfig
) -> ExtractResult:
    if isinstance(request, IngestContent):
        logger.info("Extracting from uploaded content {}", request)
        return await extract_content(
            request.content_bytes,
            filename=request.filename,
            mimetype=request.content_type,
            extract_tables=collection_config.extract_tables,
            extract_images=collection_config.extract_images,
        )
    elif isinstance(request, IngestURL):
        logger.info(
            "Extracting content from url '{}'",
            request.url,
        )
        return await extract_url(
            request.url,
            extract_tables=collection_config.extract_tables,
            extract_images=collection_config.extract_images,
        )
    else:
        raise ValueError(f"Ingest expected URL or Content, but was {request}")


async def _chunk(extracted: str) -> List[str]:
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    return splitter.split_text(extracted)


async def _embed_text(
    text_chunks: List[Tuple[int, str]],
    collection_config: CollectionConfig,
    config: ServeConfig,
) -> List[embeddings.TextEmbedding]:
    embedding = text_embedding_model(collection_config.text_embedding_model, config)
    text_embeddings = await embedding.aembed_documents([text for _, text in text_chunks])

    return [
        embeddings.TextEmbedding(
            chunk_id=chunk_id,
            text=text,
            embedding=embedding,
        )
        for ((chunk_id, text), embedding) in zip(text_chunks, text_embeddings, strict=True)
    ]

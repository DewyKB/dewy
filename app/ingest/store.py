from typing import Annotated

from fastapi import Depends, Request
from llama_index import ServiceContext, StorageContext, VectorStoreIndex
from llama_index.embeddings import BaseEmbedding
from llama_index.ingestion import DocstoreStrategy, IngestionPipeline
from llama_index.ingestion.cache import IngestionCache, RedisCache
from llama_index.storage.docstore.redis_docstore import RedisDocumentStore
from llama_index.vector_stores import RedisVectorStore
from loguru import logger

from app.config import settings

DEFAULT_OPENAI_EMBEDDING_MODEL: str = "text-embedding-ada-002"
DEFAULT_HF_EMBEDDING_MODEL: str = "BAAI/bge-small-en"
DEFAULT_OPENAI_LLM_MODEL: str = "gpt-3.5-turbo"
DEFAULT_HF_LLM_MODEL: str = "StabilityAI/stablelm-tuned-alpha-3b"


def _embedding_model(model: str) -> BaseEmbedding:
    if not model:
        if settings.OPENAI_API_KEY:
            model = "openai"
        else:
            model = "local"

    split = model.split(":", 2)
    if split[0] == "openai":
        from llama_index.embeddings import OpenAIEmbedding

        model = DEFAULT_OPENAI_EMBEDDING_MODEL
        if len(split) == 2:
            model = split[1]
        return OpenAIEmbedding(model=model)
    elif split[0] == "local":
        from llama_index.embeddings import HuggingFaceEmbedding

        model = DEFAULT_HF_EMBEDDING_MODEL
        if len(split) == 2:
            model = split[1]
        return HuggingFaceEmbedding(model)
    elif split[0] == "ollama":
        from llama_index.embeddings import OllamaEmbedding

        model = split[1]
        return OllamaEmbedding(
            model=model, base_url=settings.OLLAMA_BASE_URL.unicode_string()
        )
    else:
        raise ValueError(f"Unrecognized embedding model '{model}'")


def _llm_model(model: str) -> BaseEmbedding:
    if not model:
        if settings.OPENAI_API_KEY:
            model = "openai"
        else:
            model = "local"

    split = model.split(":", 2)
    if split[0] == "openai":
        from llama_index.llms import OpenAI

        model = DEFAULT_OPENAI_LLM_MODEL
        if len(split) == 2:
            model = split[1]
        return OpenAI(model=model)
    elif split[0] == "local":
        from llama_index.llms import HuggingFaceLLM

        model = DEFAULT_HF_LLM_MODEL
        if len(split) == 2:
            model = split[1]
        return HuggingFaceLLM(model_name=model, tokenizer_name=model)
    elif split[0] == "ollama":
        from llama_index.llms import Ollama

        model = split[1]
        return Ollama(model=model, base_url=settings.OLLAMA_BASE_URL.unicode_string())
    else:
        raise ValueError(f"Unrecognized LLM model '{model}")


class Store:
    """Class managing the vector and document store."""

    def __init__(self) -> None:
        self.embedding = _embedding_model(settings.EMBEDDING_MODEL)
        self.llm = _llm_model(settings.LLM_MODEL)
        logger.info("Embedding: {}", self.embedding.to_dict())
        logger.info("LLM: {}", self.llm.to_dict())

        vector_store = RedisVectorStore(
            index_name="vector_store",
            redis_url=settings.REDIS.unicode_string(),
        )

        docstore = RedisDocumentStore.from_redis_client(
            vector_store.client,
            namespace="document_store",
        )

        cache = IngestionCache(
            cache=RedisCache.from_redis_client(vector_store.client),
        )

        storage_context = StorageContext.from_defaults(
            vector_store=vector_store, docstore=docstore
        )

        from llama_index.node_parser import HierarchicalNodeParser

        transformations = [
            HierarchicalNodeParser.from_defaults(chunk_sizes=[2048, 512, 128]),
        ]

        if self.llm:
            # Transformations that require an LLM.
            from llama_index.extractors import SummaryExtractor, TitleExtractor

            transformations.extend(
                [
                    TitleExtractor(self.llm),
                    SummaryExtractor(self.llm),
                ]
            )

        self.service_context = ServiceContext.from_defaults(
            llm=self.llm,
            embed_model=self.embedding,
            transformations=transformations,
        )

        self.index = VectorStoreIndex(
            [],
            service_context=self.service_context,
            storage_context=storage_context,
        )

        self.ingestion_pipeline = IngestionPipeline(
            transformations=transformations + [self.embedding],
            vector_store=vector_store,
            docstore=docstore,
            cache=cache,
            docstore_strategy=DocstoreStrategy.UPSERTS,
        )


def _store(request: Request) -> Store:
    # The store was set on the state by the `lifespan` method on the service.
    return request.state.store


StoreDep = Annotated[Store, Depends(_store)]

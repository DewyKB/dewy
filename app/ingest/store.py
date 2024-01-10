from typing import Annotated

from fastapi import Depends, Request
from llama_index import ServiceContext, StorageContext, VectorStoreIndex
from llama_index.ingestion import DocstoreStrategy, IngestionPipeline
from llama_index.ingestion.cache import IngestionCache, RedisCache
from llama_index.storage.docstore.redis_docstore import RedisDocumentStore
from llama_index.vector_stores import RedisVectorStore

from app.config import settings
from app.ingest.embed import EMBED_MODEL


class Store:
    """Class managing the vector and document store."""

    def __init__(self) -> None:
        from llama_index.llms import HuggingFaceLLM
        self.llm = HuggingFaceLLM(
            model_name = "/models/llm",
            tokenizer_name = "/models/llm")

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
            embed_model=EMBED_MODEL,
            transformations=transformations,
        )

        self.index = VectorStoreIndex(
            [],
            service_context=self.service_context,
            storage_context=storage_context,
        )

        self.ingestion_pipeline = IngestionPipeline(
            transformations=transformations + [EMBED_MODEL],
            vector_store=vector_store,
            docstore=docstore,
            cache=cache,
            docstore_strategy=DocstoreStrategy.UPSERTS,
        )


def _store(request: Request) -> Store:
    # The store was set on the state by the `lifespan` method on the service.
    return request.state.store


StoreDep = Annotated[Store, Depends(_store)]

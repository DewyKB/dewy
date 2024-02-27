import dataclasses
from typing import Callable

from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_openai import OpenAIEmbeddings

from dewy.config import Config


@dataclasses.dataclass
class EmbeddingModel:
    name: str
    dimensions: int
    factory: Callable[[Config], Embeddings]


EMBEDDINGS = {
    e.name: e
    for e in [
        EmbeddingModel(
            name="openai:text-embedding-ada-002",
            dimensions=1536,
            factory=lambda config: OpenAIEmbeddings(
                model="text-embedding-ada-002", api_key=config.OPENAI_API_KEY
            ),
        ),
        EmbeddingModel(
            name="hf:BAAI/bge-small-en",
            dimensions=384,
            factory=lambda _config: HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en"),
        ),
        EmbeddingModel(
            name="hf:BAAI/bge-small-en-v1.5",
            dimensions=384,
            factory=lambda _config: HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en-v1.5"),
        ),
    ]
}

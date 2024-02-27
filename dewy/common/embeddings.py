import dataclasses
from typing import Callable

from llama_index import OpenAIEmbedding
from llama_index.embeddings import BaseEmbedding, HuggingFaceEmbedding

from dewy.config import Config


@dataclasses.dataclass
class EmbeddingModel:
    name: str
    dimensions: int
    factory: Callable[[Config], BaseEmbedding]


EMBEDDINGS = {
    e.name: e
    for e in [
        EmbeddingModel(
            name="openai:text-embedding-ada-002",
            dimensions=1536,
            factory=lambda config: OpenAIEmbedding(
                model="text-embedding-ada-002",
                api_key=config.OPENAI_API_KEY
            ),
        ),
        EmbeddingModel(
            name="hf:BAAI/bge-small-en",
            dimensions=384,
            factory=lambda _config: HuggingFaceEmbedding("BAAI/bge-small-en"),
        ),
        EmbeddingModel(
            name="hf:BAAI/bge-small-en-v1.5",
            dimensions=384,
            factory=lambda _config: HuggingFaceEmbedding("BAAI/bge-small-en-v1.5"),
        ),
    ]
}

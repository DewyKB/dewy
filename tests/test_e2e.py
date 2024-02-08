import random
import string
import time
from typing import BinaryIO

import pytest
from dewy_client.api.default import (
    add_collection,
    add_document_from_content,
    add_document_from_url,
    get_document,
    get_document_status,
    list_chunks,
    retrieve_chunks,
)
from dewy_client.models import (
    AddDocumentContentRequest,
    AddDocumentUrlRequest,
    CollectionCreate,
    IngestState,
    RetrieveRequest,
)
from dewy_client.types import File

from tests.conftest import NEARLY_EMPTY_BYTES, NEARLY_EMPTY_PATH

SKELETON_OF_THOUGHT_PDF = "https://arxiv.org/pdf/2307.15337.pdf"


@pytest.mark.parametrize(
    "embedding_model", ["openai:text-embedding-ada-002", "hf:BAAI/bge-small-en"]
)
@pytest.mark.timeout(120)  # slow due to embedding (especially in CI)
async def test_index_retrieval(client, embedding_model):
    name = "".join(random.choices(string.ascii_lowercase, k=5))

    collection = await add_collection.asyncio(
        client=client,
        body=CollectionCreate(name=name, text_embedding_model=embedding_model),
    )

    document = await add_document_from_content.asyncio(
        client=client,
        body=AddDocumentContentRequest(
            content = File(payload=NEARLY_EMPTY_BYTES,
                           file_name = "nearly_empty.pdf"),
            collection_id=collection.id
        ),
    )

    status = None
    while getattr(status, "ingest_state", IngestState.PENDING) == IngestState.PENDING:
        time.sleep(0.5)
        status = await get_document_status.asyncio(document.id, client=client)

    document = await get_document.asyncio(document.id, client=client)
    assert document.extracted_text.startswith("Skeleton-of-Thought")

    chunks = await list_chunks.asyncio(
        client=client, collection_id=collection.id, document_id=document.id
    )
    assert len(chunks) > 0
    assert chunks[0].document_id == document.id

    retrieved = await retrieve_chunks.asyncio(
        client=client,
        body=RetrieveRequest(
            collection_id=collection.id,
            query="outline the steps to using skeleton-of-thought prompting",
        ),
    )
    assert len(retrieved.text_results) > 0

    assert retrieved.text_results[0].document_id == document.id
    assert "skeleton" in retrieved.text_results[0].text.lower()


async def test_ingest_error(client):
    name = "".join(random.choices(string.ascii_lowercase, k=5))

    collection = await add_collection.asyncio(
        client=client,
        body=CollectionCreate(name=name, text_embedding_model="hf:BAAI/bge-small-en"),
    )

    MESSAGE = "expected-test-failure"
    document = await add_document_from_url.asyncio(
        client=client,
        body=AddDocumentUrlRequest(url=f"error://{MESSAGE}", collection_id=collection.id),
    )

    status = None
    while getattr(status, "ingest_state", IngestState.PENDING) == IngestState.PENDING:
        time.sleep(0.2)
        status = await get_document_status.asyncio(document.id, client=client)

    assert status.ingest_state == IngestState.FAILED
    assert status.ingest_error == MESSAGE

    document = await get_document.asyncio(document.id, client=client)
    assert document.ingest_state == IngestState.FAILED
    assert document.ingest_error == MESSAGE

    chunks = await list_chunks.asyncio(
        client=client, collection_id=collection.id, document_id=document.id
    )
    assert len(chunks) == 0

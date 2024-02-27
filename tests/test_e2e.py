import asyncio
import random
import string

import pytest
from dewy_client.api.kb import (
    add_collection,
    add_document,
    get_document,
    get_document_status,
    list_chunks,
    retrieve_chunks,
    upload_document_content,
)
from dewy_client.models import (
    CollectionCreate,
    IngestState,
    RetrieveRequest,
)
from dewy_client.models.add_document_request import AddDocumentRequest
from dewy_client.models.body_upload_document_content import BodyUploadDocumentContent
from dewy_client.types import File

from tests.conftest import NEARLY_EMPTY_BYTES, NEARLY_EMPTY_TEXT

SKELETON_OF_THOUGHT_PDF = "https://arxiv.org/pdf/2307.15337.pdf"


@pytest.mark.parametrize(
    "embedding_model", ["openai:text-embedding-ada-002", "hf:BAAI/bge-small-en", "hf:BAAI/bge-small-en-v1.5"]
)
@pytest.mark.timeout(120)  # slow due to embedding (especially in CI)
async def test_index_retrieval(client, embedding_model):
    collection_name = "".join(random.choices(string.ascii_lowercase, k=5))

    collection = await add_collection.asyncio(
        client=client,
        body=CollectionCreate(name=collection_name, text_embedding_model=embedding_model),
    )

    assert NEARLY_EMPTY_BYTES

    document = await add_document.asyncio(
        client=client, body=AddDocumentRequest(collection=collection.name)
    )
    document = await upload_document_content.asyncio(
        document.id,
        client=client,
        body=BodyUploadDocumentContent(
            content=File(
                payload=NEARLY_EMPTY_BYTES,
                file_name="nearly_empty.pdf",
                mime_type="application/pdf",
            ),
        ),
    )

    status = None
    while getattr(status, "ingest_state", IngestState.PENDING) == IngestState.PENDING:
        await asyncio.sleep(0.5)
        status = await get_document_status.asyncio(document.id, client=client)

    document = await get_document.asyncio(document.id, client=client)
    assert document.extracted_text.startswith(NEARLY_EMPTY_TEXT)

    chunks = await list_chunks.asyncio(
        client=client, collection=collection.name, document_id=document.id
    )
    assert len(chunks) > 0
    assert chunks[0].document_id == document.id

    retrieved = await retrieve_chunks.asyncio(
        client=client,
        body=RetrieveRequest(
            collection=collection.name,
            query="extraction",
        ),
    )
    assert len(retrieved.text_results) > 0

    assert retrieved.text_results[0].document_id == document.id
    assert "empty" in retrieved.text_results[0].text.lower()

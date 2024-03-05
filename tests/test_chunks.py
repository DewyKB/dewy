import asyncio
import random
import string
from dataclasses import dataclass

import pytest
from dewy_client.api.kb import (
    add_collection,
    add_document,
    get_document_status,
    list_chunks,
    upload_document_content,
)
from dewy_client.models.add_document_request import AddDocumentRequest
from dewy_client.models.body_upload_document_content import BodyUploadDocumentContent
from dewy_client.models import Collection, IngestState
from dewy_client.types import File

from tests.conftest import NEARLY_EMPTY_BYTES


@dataclass
class ChunkFixture:
    collection_name: str
    doc1: int
    doc2: int


async def _add_nearly_empty_doc(client, collection_name) -> int:
    doc = await add_document.asyncio(
        client=client, body=AddDocumentRequest(collection=collection_name)
    )
    await upload_document_content.asyncio(
        doc.id,
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
        await asyncio.sleep(0.2)
        status = await get_document_status.asyncio(doc.id, client=client)

    return doc.id


@pytest.fixture(scope="module")
async def chunk_fixture(client) -> ChunkFixture:
    """Adds two documents to a collection with random names."""
    collection_name = "".join(random.choices(string.ascii_lowercase, k=5))
    await add_collection.asyncio(client=client, body=Collection(name=collection_name))

    assert NEARLY_EMPTY_BYTES
    docs = await asyncio.gather(
        _add_nearly_empty_doc(client, collection_name),
        _add_nearly_empty_doc(client, collection_name),
    )
    assert len(docs) == 2
    return ChunkFixture(collection_name, doc1=docs[0], doc2=docs[1])


async def test_list_chunks_in_collection(client, chunk_fixture):
    chunks = await list_chunks.asyncio(
        client=client,
        collection=chunk_fixture.collection_name,
    )
    assert {c.document_id for c in chunks} == {chunk_fixture.doc1, chunk_fixture.doc2}


async def test_list_chunks_in_document(client, chunk_fixture):
    chunks = await list_chunks.asyncio(
        client=client,
        document_id=chunk_fixture.doc1,
    )
    assert {c.document_id for c in chunks} == {chunk_fixture.doc1}


async def test_list_chunks_in_collection_case_insensitive(client, chunk_fixture):
    upper = chunk_fixture.collection_name.upper()
    assert upper != chunk_fixture.collection_name

    chunks = await list_chunks.asyncio(
        client=client,
        collection=upper,
    )
    assert {c.document_id for c in chunks} == {chunk_fixture.doc1, chunk_fixture.doc2}


async def test_list_chunks_any_collection(client, chunk_fixture):
    pending = {chunk_fixture.doc1, chunk_fixture.doc2}
    page = 0
    while pending:
        chunks = await list_chunks.asyncio(client=client)
        assert len(chunks) > 0
        pending.difference_update({c.document_id for c in chunks})
        page += 1


async def test_list_chunks_invalid_collection(client):
    response = await list_chunks.asyncio(
        client=client,
        collection="invalid collection",
    )
    assert response == []


async def test_list_chunks_invalid_document(client, chunk_fixture):
    response = await list_chunks.asyncio(
        client=client,
        document_id=1_000_000,
    )
    assert response == []

import json
import random
import string
import time
from dataclasses import dataclass

import pytest
from dewy_client.api.kb import (
    add_collection,
    add_document,
    delete_document,
    get_document,
    get_document_status,
    list_chunks,
    list_documents,
    upload_document_content,
)
from dewy_client.models import (
    AddDocumentRequest,
    BodyUploadDocumentContent,
    Collection,
    IngestState,
)
from dewy_client.types import File

from tests.conftest import (
    NEARLY_EMPTY_BYTES,
    NEARLY_EMPTY_BYTES2,
    NEARLY_EMPTY_TEXT,
    NEARLY_EMPTY_TEXT2,
    document_ingested,
    upload_test_pdf,
)


@dataclass
class DocFixture:
    collection_name: str
    doc1: int
    doc2: int


@pytest.fixture(scope="module")
async def doc_fixture(client) -> DocFixture:
    """Adds two documents to a collection with random names."""
    collection_name = "".join(random.choices(string.ascii_lowercase, k=5))
    await add_collection.asyncio(client=client, body=Collection(name=collection_name))

    doc1 = await add_document.asyncio(
        client=client,
        body=AddDocumentRequest(collection=collection_name),
    )
    doc2 = await add_document.asyncio(
        client=client,
        body=AddDocumentRequest(collection=collection_name),
    )

    # Don't ingest anything -- we don't need them for testing documents,
    # and it's a lot faster to avoid embedding.
    return DocFixture(
        collection_name,
        doc1=doc1.id,
        doc2=doc2.id,
    )


async def test_list_documents_filtered(client, doc_fixture):
    docs = await list_documents.asyncio(client=client, collection=doc_fixture.collection_name)

    assert len(docs) == 2
    assert {doc.id for doc in docs} == {doc_fixture.doc1, doc_fixture.doc2}


async def test_list_documents_filtered_case_insensitive(client, doc_fixture):
    # Tests that using an uppercase name (when the collection is created
    # with a lower case name) still works for listing documents.

    upper_name = doc_fixture.collection_name.upper()
    assert upper_name != doc_fixture.collection_name

    docs = await list_documents.asyncio(client=client, collection=upper_name)

    assert len(docs) == 2
    assert {doc.id for doc in docs} == {doc_fixture.doc1, doc_fixture.doc2}


async def test_list_documents_unfiltered(client, doc_fixture):
    docs = await list_documents.asyncio(client=client)

    ids = {doc.id for doc in docs}
    assert doc_fixture.doc1 in ids
    assert doc_fixture.doc2 in ids


async def test_get_document(client, doc_fixture):
    document = await get_document.asyncio(doc_fixture.doc1, client=client)
    assert document
    assert document.id == doc_fixture.doc1
    assert document.ingest_state == IngestState.PENDING


async def test_get_document_invalid(client, doc_fixture):
    content = await get_document.asyncio_detailed(1_000_000, client=client)
    assert content.status_code == 404

    response_content = json.loads(content.content)
    assert response_content == {"detail": "No document with ID 1000000"}


async def test_get_document_status(client, doc_fixture):
    document = await get_document_status.asyncio(doc_fixture.doc1, client=client)
    assert document
    assert document.id == doc_fixture.doc1
    assert document.ingest_state == IngestState.PENDING


async def test_get_document_status_invalid(client, doc_fixture):
    response = await get_document_status.asyncio_detailed(1_000_000, client=client)
    assert response.status_code == 404

    response_content = json.loads(response.content)
    assert response_content == {"detail": "No document with ID 1000000"}


async def test_add_document_collection_case_insensitive(client):
    # Tests that adding a document to a collection using the name with
    # different casing (uppercase) still works.
    lower_name = "".join(random.choices(string.ascii_lowercase, k=5))

    await add_collection.asyncio(client=client, body=Collection(name=lower_name))

    upper_name = lower_name.upper()
    assert upper_name != lower_name
    doc = await add_document.asyncio(
        client=client, body=AddDocumentRequest(collection=upper_name)
    )

    docs = await list_documents.asyncio(client=client, collection=lower_name)
    assert {doc.id for doc in docs} == {doc.id}


async def test_add_document_invalid_collection(client):
    response = await add_document.asyncio_detailed(
        client=client, body=AddDocumentRequest(collection="invalid collection")
    )
    assert response.status_code == 404
    response_content = json.loads(response.content)
    assert response_content == {"detail": "No collection named 'invalid collection'"}


async def test_add_document_ingest_error(client):
    collection_name = "".join(random.choices(string.ascii_lowercase, k=5))

    collection = await add_collection.asyncio(
        client=client,
        body=Collection(name=collection_name, text_embedding_model="hf:BAAI/bge-small-en"),
    )

    MESSAGE = "expected-test-failure"
    document = await add_document.asyncio(
        client=client,
        body=AddDocumentRequest(url=f"error://{MESSAGE}", collection=collection.name),
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
        client=client, collection=collection.name, document_id=document.id
    )
    assert len(chunks) == 0


async def test_upload_document_unknown_document_id(client, doc_fixture):
    response = await upload_document_content.asyncio_detailed(
        client=client,
        document_id=1_000_000,
        body=BodyUploadDocumentContent(
            content=File(
                payload=NEARLY_EMPTY_BYTES,
                file_name="file-name-1",
                mime_type="application/pdf",
            ),
        ),
    )
    assert response.status_code == 404


async def test_document_lifecycle(client, doc_fixture):
    # 1. Upload a PDF for one of the fixutre docs and verify the document is "pending"
    await upload_test_pdf(client, doc_fixture.doc1, NEARLY_EMPTY_BYTES)

    # 2. Wait for ingestion to complete (would be nicer if we could hook into the queue somehow)
    # and verify the PDF has been ingested correctly
    await document_ingested(client, doc_fixture.doc1)

    document2 = await get_document.asyncio(doc_fixture.doc1, client=client)
    assert document2
    assert document2.id == doc_fixture.doc1
    assert document2.extracted_text == NEARLY_EMPTY_TEXT
    assert document2.url is None
    assert document2.ingest_state == IngestState.INGESTED
    assert document2.ingest_error is None

    chunks = await list_chunks.asyncio(client=client, document_id=doc_fixture.doc1)
    assert chunks

    # 3. Upload a revised PDF and verify the document is back into "pending" state
    await upload_test_pdf(client, doc_fixture.doc1, NEARLY_EMPTY_BYTES2)

    # 4. Wait for the new doc to be ingested and verify it was ingested correctly
    await document_ingested(client, doc_fixture.doc1)

    document3 = await get_document.asyncio(doc_fixture.doc1, client=client)
    assert document3
    assert document3.id == doc_fixture.doc1
    assert document3.extracted_text == NEARLY_EMPTY_TEXT2
    assert document3.url is None
    assert document3.ingest_state == IngestState.INGESTED
    assert document3.ingest_error is None

    chunks2 = await list_chunks.asyncio(client=client, document_id=doc_fixture.doc1)
    assert chunks2

    original_ids = {c.id for c in chunks}
    new_ids = {c.id for c in chunks2}
    assert original_ids.isdisjoint(new_ids)

    # 5. Verify the document and associated resources can be deleted
    await delete_document.asyncio(client=client, id=doc_fixture.doc1)
    chunks3 = await list_chunks.asyncio(client=client, document_id=doc_fixture.doc1)
    assert not chunks3


async def test_delete_document_invalid(client):
    content = await delete_document.asyncio_detailed(1_000_000, client=client)
    assert content.status_code == 404

    response_content = json.loads(content.content)
    assert response_content == {"detail": "No document with ID 1000000"}

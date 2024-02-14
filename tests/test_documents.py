from dataclasses import dataclass
import json
from pydoc import doc
import random
import string
import time

from dewy_client.api.kb import add_collection, add_document, get_document, get_document_status, list_chunks, list_collections, list_documents
from dewy_client.models import AddDocumentRequest, IngestState, CollectionCreate
import pytest

@dataclass
class DocFixture():
    collection_name: str
    doc1: int
    doc2: int

@pytest.fixture(scope="module")
async def doc_fixture(client) -> DocFixture:
    """Adds two documents to a collection with random names.
    """
    collection_name = "".join(random.choices(string.ascii_lowercase, k=5))
    await add_collection.asyncio(client=client, body=CollectionCreate(name=collection_name))

    doc1 = await add_document.asyncio(
        client=client, body=AddDocumentRequest(collection=collection_name),
    )
    doc2 = await add_document.asyncio(
        client=client, body=AddDocumentRequest(collection=collection_name),
    )

    # Don't ingest anything -- we don't need them for testing documents,
    # and it's a lot faster to avoid embedding.
    return DocFixture(
        collection_name,
        doc1 = doc1.id,
        doc2 = doc2.id,
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
    assert(response_content == {"detail": "No document with ID 1000000"})

async def test_get_document_status(client, doc_fixture):
    document = await get_document_status.asyncio(doc_fixture.doc1, client=client)
    assert document
    assert document.id == doc_fixture.doc1
    assert document.ingest_state == IngestState.PENDING

async def test_get_document_status_invalid(client, doc_fixture):
    response = await get_document_status.asyncio_detailed(1_000_000, client=client)
    assert response.status_code == 404

    response_content = json.loads(response.content)
    assert(response_content == {"detail": "No document with ID 1000000"})

async def test_add_document_collection_case_insensitive(client):
    # Tests that adding a document to a collection using the name with
    # different casing (uppercase) still works.
    lower_name = "".join(random.choices(string.ascii_lowercase, k=5))

    await add_collection.asyncio(client=client, body=CollectionCreate(name=lower_name))

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
    assert(response_content == {"detail": "No collection named 'invalid collection'"})


async def test_add_document_ingest_error(client):
    collection_name = "".join(random.choices(string.ascii_lowercase, k=5))

    collection = await add_collection.asyncio(
        client=client,
        body=CollectionCreate(name=collection_name, text_embedding_model="hf:BAAI/bge-small-en"),
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

import json
import random
import string
from dataclasses import dataclass

import pytest
from dewy_client.api.kb import (
    add_collection,
    add_document,
    delete_collection,
    get_collection,
    list_chunks,
    list_collections,
    list_documents,
)
from dewy_client.models import AddDocumentRequest, CollectionCreate

from tests.conftest import (
    NEARLY_EMPTY_BYTES,
    document_ingested,
    upload_test_pdf,
)


@dataclass
class CollectionFixture:
    collection1: string
    collection2: string


@pytest.fixture(scope="module")
async def collection_fixture(client) -> CollectionFixture:
    """Adds two collections with random names."""
    collection_name1 = "".join(random.choices(string.ascii_lowercase, k=5))
    await add_collection.asyncio(client=client, body=CollectionCreate(name=collection_name1))

    collection_name2 = "".join(random.choices(string.ascii_lowercase, k=5))
    await add_collection.asyncio(client=client, body=CollectionCreate(name=collection_name2))

    return CollectionFixture(
        collection1=collection_name1,
        collection2=collection_name2,
    )


async def test_get_collection(client):
    name = "".join(random.choices(string.ascii_lowercase, k=5))
    collection = await add_collection.asyncio(client=client, body=CollectionCreate(name=name))

    get_response = await get_collection.asyncio(collection.name, client=client)
    assert get_response.name == name
    assert get_response.text_embedding_model == "openai:text-embedding-ada-002"
    assert get_response.text_distance_metric == "cosine"


async def test_get_collection_case_insensitive(client):
    lower_name = "".join(random.choices(string.ascii_lowercase, k=5))
    await add_collection.asyncio(client=client, body=CollectionCreate(name=lower_name))

    upper_name = lower_name.upper()
    assert lower_name != upper_name

    get_response = await get_collection.asyncio(upper_name, client=client)
    assert get_response.name == lower_name
    assert get_response.text_embedding_model == "openai:text-embedding-ada-002"
    assert get_response.text_distance_metric == "cosine"


async def test_get_collection_invalid(client):
    response = await get_collection.asyncio_detailed("invalid collection", client=client)
    assert response.status_code == 404
    response_content = json.loads(response.content)
    assert response_content == {"detail": "No collection named 'invalid collection'"}


async def test_list_collection(client):
    name = "".join(random.choices(string.ascii_lowercase, k=5))
    await add_collection.asyncio(client=client, body=CollectionCreate(name=name))

    collections = await list_collections.asyncio(client=client)

    collection_row = next(x for x in collections if x.name == name)
    assert collection_row is not None
    assert collection_row.text_embedding_model == "openai:text-embedding-ada-002"
    assert collection_row.text_distance_metric == "cosine"


async def test_delete_collection(client):
    collection_name = "".join(random.choices(string.ascii_lowercase, k=5))
    await add_collection.asyncio(client=client, body=CollectionCreate(name=collection_name))

    await delete_collection.asyncio(client=client, name=collection_name)

    collections = await list_collections.asyncio(client=client)
    assert collection_name not in [c.name for c in collections]


async def test_delete_unknown_collection(client):
    response = await delete_collection.asyncio_detailed("invalid collection", client=client)
    assert response.status_code == 404
    response_content = json.loads(response.content)
    assert response_content == {"detail": "No collection named 'invalid collection'"}


async def test_collection_lifecycle(client):
    # 1. Create a collection
    collection_name = "".join(random.choices(string.ascii_lowercase, k=5))
    await add_collection.asyncio(client=client, body=CollectionCreate(name=collection_name))

    # 1. Create a document in the collection
    doc = await add_document.asyncio(
        client=client,
        body=AddDocumentRequest(collection=collection_name),
    )

    # 2. Upload a PDF for the doc and verify the document is "pending"
    await upload_test_pdf(client, doc.id, NEARLY_EMPTY_BYTES)

    # 3. Wait for ingestion to complete (would be nicer if we could hook into the queue somehow)
    # and verify the PDF has been ingested correctly
    await document_ingested(client, doc.id)

    chunks = await list_chunks.asyncio(client=client, document_id=doc.id)
    assert chunks

    # 4. Delete the collection and verify it removes documents & chunks
    await delete_collection.asyncio(client=client, name=collection_name)

    collections = await list_collections.asyncio(client=client)
    assert collection_name not in [c.name for c in collections]

    documents = await list_documents.asyncio(client=client, collection=collection_name)
    assert not documents

    chunks = await list_chunks.asyncio(client=client, collection=collection_name)
    assert not chunks

import json
import random
import string
from dataclasses import dataclass

import pytest
from dewy_client.api.kb import add_collection, get_collection, list_collections, delete_collection
from dewy_client.models import CollectionCreate


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

async def test_delete_collection(client, collection_fixture):
    await delete_collection.asyncio(client=client, name=collection_fixture.collection1)

    collections = await list_collections.asyncio(client=client)
    assert collection_fixture.collection1 not in [c.name for c in collections]
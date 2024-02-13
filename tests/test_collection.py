import random
import string

from dewy_client.api.kb import add_collection, get_collection, list_collections
from dewy_client.models import CollectionCreate


async def test_create_collection(client):
    name = "".join(random.choices(string.ascii_lowercase, k=5))
    collection = await add_collection.asyncio(client=client, body=CollectionCreate(name=name))

    assert collection.name == name
    assert collection.text_embedding_model == "openai:text-embedding-ada-002"
    assert collection.text_distance_metric == "cosine"

    collection_id = collection.id

    list_response = await list_collections.asyncio(client=client)

    # "find" the collection with the new collection ID, since
    # other tests may have created other collections
    collection_row = next(x for x in list_response if x.id == collection_id)
    assert collection_row is not None
    assert collection_row.name == name

    get_response = await get_collection.asyncio(collection_id, client=client)

    assert get_response.name == name


async def test_find_collection(client):
    name = "".join(random.choices(string.ascii_lowercase, k=5))
    collection1 = await add_collection.asyncio(
        client=client, body=CollectionCreate(name=f"{name}")
    )
    _collection2 = await add_collection.asyncio(
        client=client, body=CollectionCreate(name=f"{name}-1")
    )

    list_response = await list_collections.asyncio(name=f"{name}", client=client)
    assert len(list_response) == 1
    assert list_response[0].id == collection1.id

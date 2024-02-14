import random
import string

from dewy_client.api.kb import add_collection, get_collection, list_collections
from dewy_client.models import CollectionCreate


async def test_create_collection(client):
    id = "".join(random.choices(string.ascii_lowercase, k=5))
    collection = await add_collection.asyncio(client=client, body=CollectionCreate(id=id))

    assert collection.id == id
    assert collection.text_embedding_model == "openai:text-embedding-ada-002"
    assert collection.text_distance_metric == "cosine"

    list_response = await list_collections.asyncio(client=client)

    # "find" the collection with the new collection ID, since
    # other tests may have created other collections
    collection_row = next(x for x in list_response if x.id == collection_id)
    assert collection_row is not None

    get_response = await get_collection.asyncio(id, client=client)

    assert get_response.id == id
    assert get_response.text_embedding_model == "openai:text-embedding-ada-002"
    assert get_response.text_distance_metric == "cosine"


async def test_find_collection(client):
    id = "".join(random.choices(string.ascii_lowercase, k=5))
    collection1 = await add_collection.asyncio(
        client=client, body=CollectionCreate(id=f"{id}")
    )
    _collection2 = await add_collection.asyncio(
        client=client, body=CollectionCreate(id=f"{id}-1")
    )

    list_response = await list_collections.asyncio(id=f"{id}", client=client)
    assert len(list_response) == 1
    assert list_response[0].id == collection1.id

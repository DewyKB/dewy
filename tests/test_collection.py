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

    # Test list collections.
    list_response = await list_collections.asyncio(client=client)
    collection_row = next(x for x in list_response if x.name == name)
    assert collection_row is not None
    assert collection_row.text_embedding_model == "openai:text-embedding-ada-002"
    assert collection_row.text_distance_metric == "cosine"

    # Test get collection
    get_response = await get_collection.asyncio(name, client=client)
    assert get_response.name == name
    assert get_response.text_embedding_model == "openai:text-embedding-ada-002"
    assert get_response.text_distance_metric == "cosine"

import random
import string


async def test_create_collection(client):
    name = "".join(random.choices(string.ascii_lowercase, k=5))
    create_response = await client.put("/api/collections/", json={"name": name})
    assert create_response.status_code == 200

    json = create_response.json()
    assert json["name"] == name
    assert json["text_embedding_model"] == "openai:text-embedding-ada-002"
    assert json["text_distance_metric"] == "cosine"

    collection_id = json["id"]

    list_response = await client.get("/api/collections/")
    assert list_response.status_code == 200

    # "find" the collection with the new collection ID, since
    # other tests may have created other collections
    json = list_response.json()
    collection_row = next(x for x in list_response.json() if x["id"] == collection_id)
    assert collection_row is not None
    assert collection_row["name"] == name

    get_response = await client.get(f"/api/collections/{collection_id}")
    assert get_response.status_code == 200

    json = get_response.json()
    assert collection_row["name"] == name

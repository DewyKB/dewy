async def test_create_collection(client):
    response = await client.put("/api/collections/", json={"name": "my_collection"})
    assert response.status_code == 200

    json = response.json()
    assert json["name"] == "my_collection"
    assert json["text_embedding_model"] == "openai:text-embedding-ada-002"
    assert json["text_distance_metric"] == "cosine"

    collection_id = json["id"]
    assert collection_id == 1

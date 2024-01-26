async def test_create_collection(client):
    response = await client.put("/api/collections/", json={"name": "my_collection"})
    print(response)
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

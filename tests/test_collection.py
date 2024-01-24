async def test_read_main(client):
    response = await client.get("/collections/")
    print(response)
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
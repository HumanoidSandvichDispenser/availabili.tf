def test_set_username(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.post(
        "/api/user/username",
        json={
            "username": "NewUsername"
        },
        headers=headers)
    assert response.json["username"] == "NewUsername"

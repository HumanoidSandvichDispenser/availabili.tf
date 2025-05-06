import app_db
from login import extract_steam_id_from_response, generate_base36


def test_initial_state(client):
    from models.auth_session import AuthSession
    assert app_db.db.session.query(AuthSession).count() == 1

def test_get_user(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.get(
        "/api/login/get-user",
        headers=headers
    )
    assert response.status_code == 200

def test_generate_base36():
    string = generate_base36(8)
    assert len(string) == 8

def test_extract_steam_id_from_response():
    response = "http://steamcommunity.com/openid/id/76561198248436608"
    steam_id = extract_steam_id_from_response(response)
    assert steam_id == "76561198248436608"

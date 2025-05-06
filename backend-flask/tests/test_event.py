import datetime
from models.event import Event
from app_db import db
from models.player_event import PlayerEvent


def test_get_event(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.get(
        "/api/events/1",
        headers=headers)
    assert response.json["name"] == "Test event"

def test_get_team_events(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.get(
        "/api/events/team/id/1",
        headers=headers)
    assert len(response.json) == 1

def test_create_event(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.post(
        "/api/events/team/id/1",
        json={
            "name": "New Event",
            "description": "Test event description",
            "startTime": 0,
            "playerRoles": [
                {
                    "player": {
                        "steamId": "76561198248436608",
                        "username": "pyro from csgo",
                    },
                    "role": {
                        "role": "Pyro",
                        "isMain": False,
                    },
                }
            ]
        },
        headers=headers)
    assert response.json["name"] == "New Event"

def test_update_event(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.patch(
        "/api/events/1",
        json={
            "name": "Updated Event",
            "description": "Updated description",
            "startTime": 0,
            "playerRoles": [],
        },
        headers=headers)
    print(response)
    assert response.json["name"] == "Updated Event"

def test_delete_event(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.delete(
        "/api/events/1",
        headers=headers)
    assert db.session.query(Event).where(Event.id == 1).one_or_none() is None

def test_get_maximum_matching_1_player(app):
    event = db.session.query(Event).first()
    assert event.get_maximum_matching() == 1

def test_get_maximum_matching_no_players(app):
    event = Event(
        team_id=1,
        name="New Event",
        start_time=datetime.datetime.now(datetime.timezone.utc),
    )
    assert event.get_maximum_matching() == 0

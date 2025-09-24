import datetime
from models.event import Event
from app_db import db
from models.player import Player
from models.player_event import PlayerEvent
from models.player_team import PlayerTeam


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

def test_get_discord_content(app):
    def populate_team():
        player2 = Player(steam_id=76561198248436609, username="pyro from cs2")
        player3 = Player(steam_id=76561198248436610, username="pyro from cs3")
        player4 = Player(steam_id=76561198248436611, username="pyro from cs4")

        db.session.add(player2)
        db.session.add(player3)
        db.session.add(player4)
        db.session.flush()

        player_team2 = PlayerTeam(
            player_id=player2.steam_id,
            team_id=1,
        )
        player_team3 = PlayerTeam(
            player_id=player3.steam_id,
            team_id=1,
        )
        player_team4 = PlayerTeam(
            player_id=player4.steam_id,
            team_id=1,
        )
        db.session.add(player_team2)
        db.session.add(player_team3)
        db.session.add(player_team4)
        db.session.commit()

    populate_team()
    event = Event(
        team_id=1,
        name="New Event",
        start_time=datetime.datetime.now(datetime.timezone.utc),
    )
    db.session.add(event)
    db.session.flush()
    event_player = PlayerEvent(
        event_id=event.id,
        player_id=76561198248436608,
        player_team_role_id=1,
        has_confirmed=True,
    )
    event_player2 = PlayerEvent(
        event_id=event.id,
        player_id=76561198248436609,
        player_team_role_id=None,
        has_confirmed=True,
    )
    event_player3 = PlayerEvent(
        event_id=event.id,
        player_id=76561198248436610,
        player_team_role_id=None,
        has_confirmed=False,
    )
    event_player4 = PlayerEvent(
        event_id=event.id,
        player_id=76561198248436611,
        player_team_role_id=None,
        has_confirmed=False,
    )
    db.session.add(event_player)
    db.session.add(event_player2)
    db.session.add(event_player3)
    db.session.add(event_player4)
    db.session.commit()

    content = event.get_discord_content()
    assert "✅ pyro from csgo" in content
    assert "✅ pyro from cs2" in content
    assert "⌛ pyro from cs3, pyro from cs4" in content


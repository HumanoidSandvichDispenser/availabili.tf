import pytest
import app_db
from models.team import Team


def test_create_team(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.post(
        "/api/team/",
        json={
            "teamName": "Test Team",
            "leagueTimezone": "America/New_York",
            "minuteOffset": 30,
        },
        headers=headers)
    assert response.json["team"]["teamName"] == "Test Team"

def test_create_team_invalid(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.post(
        "/api/team/",
        json={ },
        headers=headers)
    assert response.status_code == 422

#def test_update_team(client, headers):
#    client.set_cookie("auth", "test_key")
#    response = client.patch(
#        "/api/team/id/1/",
#        json={
#            "teamName": "Updated Team Name",
#            "leagueTimezone": "America/New_York",
#            "minuteOffset": 30,
#        },
#        headers=headers)
#    assert response.json["teamName"] == "Updated Team Name"

#def test_remove_team_member(client, headers):
#    client.set_cookie("auth", "test_key")
#    response = client.delete(
#        "/api/team/id/1/player/76561198248436608/",
#        headers=headers)
#    assert response.status_code == 200

def test_view_teams(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.get(
        "/api/team/all/",
        headers=headers)
    assert len(response.json["teams"]) > 0

def test_view_team_by_id(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.get(
        "/api/team/id/1/",
        headers=headers)
    assert response.json["team"]["teamName"] == "Team Pepeja"

def test_edit_member_roles(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.patch(
        "/api/team/id/1/edit-player/76561198248436608",
        json={
            "roles": [
                {
                    "role": "Pyro",
                    "isMain": False,
                }
            ],
        },
        headers=headers)

    assert response.status_code == 204

def test_make_player_team_leader(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.put(
        "/api/team/id/1/player/76561198248436608/",
        json={},
        headers=headers)
    assert response.status_code == 500 # not implemented

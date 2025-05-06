import datetime

import pytest
import app_db
from models.auth_session import AuthSession
from models.match import RawLogDetails
from models.player import Player
from models.player_team import PlayerTeam
from models.player_team_availability import PlayerTeamAvailability
from models.team import Team
from unittest.mock import Mock, patch
from requests.models import Response
from requests import Request

from models.team_match import TeamMatch


## Integration test 1: team creation

def test_create_team(client, headers):
    client.set_cookie("auth", "test_key")
    client.post(
        "/api/team/",
        json={
            "teamName": "Test Team",
            "leagueTimezone": "America/New_York",
            "minuteOffset": 30,
        },
        headers=headers)
    assert app_db.db.session.query(Team).where(Team.team_name == "Test Team").one_or_none() is not None

def test_create_team_player_added_as_tl(client, headers):
    client.set_cookie("auth", "test_key")
    client.post(
        "/api/team/",
        json={
            "teamName": "Test Team",
            "leagueTimezone": "America/New_York",
            "minuteOffset": 30,
        },
        headers=headers)
    team_id = app_db.db.session.query(Team).where(Team.team_name == "Test Team").one().id
    player_team = app_db.db.session.query(
        PlayerTeam
    ).where(
        PlayerTeam.team_id == team_id
    ).one()

    assert player_team.is_team_leader

## Integration test 2: leaving team

def test_leaving_team_deletes_team(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.delete(
        "/api/team/id/1/player/76561198248436608/",
        headers=headers)
    assert app_db.db.session.query(Team).where(Team.id == 1).one_or_none() is None

## Integration test 3: availability scheduling

def test_availability_scheduling(client, headers):
    client.set_cookie("auth", "test_key")
    response = client.put(
        "/api/schedule/",
        json={
            "teamId": 1,
            "availability": [1] * 168,
            "windowStart": "2024-10-01T00:30:00Z",
        },
        headers=headers,
    )
    pta = app_db.db.session.query(
        PlayerTeamAvailability
    ).where(
        PlayerTeamAvailability.player_team_id == 1,
    ).one()

    assert pta.end_time == datetime.datetime(2024, 10, 8, 0, 30, tzinfo=datetime.timezone.utc)

def test_availability_merge(client, headers):
    client.set_cookie("auth", "test_key")
    client.put(
        "/api/schedule/",
        json={
            "teamId": 1,
            "availability": [1] * 168,
            "windowStart": "2024-10-01T00:30:00Z",
        },
        headers=headers,
    )
    client.put(
        "/api/schedule/",
        json={
            "teamId": 1,
            "availability": [1] * 168,
            "windowStart": "2024-10-08T00:30:00Z",
        },
        headers=headers,
    )

    ptas = app_db.db.session.query(
        PlayerTeamAvailability
    ).where(
        PlayerTeamAvailability.player_team_id == 1,
    ).all()

    assert len(ptas) == 1

def test_availability_split(client, headers):
    client.set_cookie("auth", "test_key")
    client.put(
        "/api/schedule/",
        json={
            "teamId": 1,
            "availability": [1] * 168,
            "windowStart": "2024-10-01T00:30:00Z",
        },
        headers=headers,
    )
    client.put(
        "/api/schedule/",
        json={
            "teamId": 1,
            "availability": [0] * 4 + [1] * 164,
            "windowStart": "2024-10-01T04:30:00Z",
        },
        headers=headers,
    )

    pta = app_db.db.session.query(
        PlayerTeamAvailability
    ).where(
        PlayerTeamAvailability.player_team_id == 1,
    ).first()

    assert pta is not None
    assert pta.end_time == datetime.datetime(2024, 10, 1, 4, 30, tzinfo=datetime.timezone.utc)

## Integration test 4: ETL job

@pytest.fixture
def mock_example_log() -> RawLogDetails:
    return {
        "teams": {
            "Blue": {"score": 1},
            "Red": {"score": 2},
        },
        "players": {
            "[U:1:288170880]": {
                "team": "Blue",
                "kills": 0,
                "deaths": 1,
                "assists": 0,
                "dmg": 0,
                "dt": 0,
            },
        },
        "info": {
            "title": "Test Match",
            "date": int(datetime.datetime.now(datetime.timezone.utc).timestamp()),
            "map": "cp_process_f12",
        },
        "length": 3600,
    }

def test_transform_load(client, app, mock_example_log):
    from jobs.fetch_logstf import transform

    team_id = 1

    # patch celery task to avoid sending a task to the queue
    with patch("jobs.fetch_logstf.update_playtime.delay", return_value=None):
        for instance in transform(1, mock_example_log, None, team_id):
            app_db.db.session.add(instance)
        app_db.db.session.commit()

    team_match = app_db.db.session.query(
        TeamMatch
    ).where(
        TeamMatch.team_id == team_id,
    ).one()

    assert len(team_match.match.players) == 1

def test_transform_load_no_team(client, app, mock_example_log):
    from jobs.fetch_logstf import transform

    team_id = 1

    # patch celery task to avoid sending a task to the queue
    with patch("jobs.fetch_logstf.update_playtime.delay", return_value=None):
        for instance in transform(1, mock_example_log, None, None):
            app_db.db.session.add(instance)
        app_db.db.session.commit()

    team_match = app_db.db.session.query(
        TeamMatch
    ).where(
        TeamMatch.team_id == team_id,
    ).one_or_none()

    assert team_match is None

## Integration test 5: OpenID

@pytest.fixture
def mock_openid():
    return {
        "openid.ns": "http://specs.openid.net/auth/2.0",
        "openid.mode": "id_res",
        "openid.op_endpoint": "https://steamcommunity.com/openid/login",
        "openid.claimed_id": "https://steamcommunity.com/openid/id/76561198248436608",
        "openid.identity": "https://steamcommunity.com/openid/id/76561198248436608",
        "openid.return_to": "https://availabili-tf.sandvich.xyz/login",
        "openid.response_nonce": "2025-05-06T16:58:39ZPoXodsvJwAB/SEAs6xwz25rZvmU=",
        "openid.assoc_handle": "1234567890",
        "openid.signed": "signed,op_endpoint,claimed_id,identity,return_to,response_nonce,assoc_handle",
        "openid.sig": "GI2sIIWma7SR0Jz/tQfTKzUie/o="
    }

def test_steam_authenticate_new_auth_token(client, headers, mock_openid):
    client.set_cookie("auth", "test_key")

    # patch requests.get
    mock = Mock()
    mock.status_code = 200
    mock.headers = {"Content-Type": "application/json"}
    mock.text = "openid.ns:http://specs.openid.net/auth/2.0\nis_valid:true\n"

    auth_session_count = app_db.db.session.query(AuthSession).count()

    with patch("requests.post", return_value=mock):
        client.post(
            "/api/login/authenticate",
            json=mock_openid,
            headers=headers)

        assert app_db.db.session.query(AuthSession).count() == auth_session_count + 1

def test_steam_authenticate_new_user(client, headers, mock_openid):
    client.set_cookie("auth", "test_key")

    # patch requests.get
    mock = Mock()
    mock.status_code = 200
    mock_openid["openid.claimed_id"] = "https://steamcommunity.com/openid/id/123"
    mock_openid["openid.identity"] = "https://steamcommunity.com/openid/id/123"
    mock.headers = {"Content-Type": "application/json"}
    mock.text = "openid.ns:http://specs.openid.net/auth/2.0\nis_valid:true\n"

    with patch("requests.post", return_value=mock):
        client.post(
            "/api/login/authenticate",
            json=mock_openid,
            headers=headers)

        assert app_db.db.session.query(Player).where(Player.steam_id == 123).one() is not None

def test_steam_authenticate_fail(client, headers, mock_openid):
    client.set_cookie("auth", "test_key")

    # patch requests.get
    mock = Mock()
    mock.status_code = 401
    mock.headers = {"Content-Type": "application/json"}
    mock.text = "openid.ns:http://specs.openid.net/auth/2.0\nis_valid:false\n"

    auth_session_count = app_db.db.session.query(AuthSession).count()

    with patch("requests.post", return_value=mock):
        client.post(
            "/api/login/authenticate",
            json=mock_openid,
            headers=headers)

        assert app_db.db.session.query(AuthSession).count() == auth_session_count

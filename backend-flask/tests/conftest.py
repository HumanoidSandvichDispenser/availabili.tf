import datetime
from flask import Blueprint
import pytest
import app_db
from unittest.mock import patch

from models.auth_session import AuthSession
from models.event import Event
from models.player import Player
from models.player_event import PlayerEvent
from models.player_team import PlayerTeam
from models.player_team_role import PlayerTeamRole
from models.team import Team
from models.team_integration import TeamLogsTfIntegration

@pytest.fixture()
def app():
    flask_app = app_db.create_app()
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    db = app_db.db

    import login
    import schedule
    import team
    import user
    import events
    import match

    api = Blueprint("api", __name__, url_prefix="/api")
    api.register_blueprint(login.api_login)
    api.register_blueprint(schedule.api_schedule)
    api.register_blueprint(team.api_team)
    api.register_blueprint(user.api_user)
    api.register_blueprint(events.api_events)
    api.register_blueprint(match.api_match)

    flask_app.register_blueprint(api)

    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()
        populate_db(db)

        yield flask_app

        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture
def mock_get():
    with patch("requests.get") as _mock_get:
        yield _mock_get

@pytest.fixture
def mock_post():
    with patch("requests.post") as _mock_post:
        yield _mock_post

@pytest.fixture
def headers():
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": "auth=test_key",
    }

def populate_db(db):
    player = Player(steam_id=76561198248436608, username="pyro from csgo")
    team = Team(team_name="Team Pepeja", tz_timezone="America/New_York", minute_offset=30)

    db.session.add(player)
    db.session.add(team)

    db.session.flush()

    player_team = PlayerTeam(
        player_id=player.steam_id,
        team_id=team.id,
        team_role=PlayerTeam.TeamRole.Player,
        is_team_leader=True,
    )
    logs_tf_integration = TeamLogsTfIntegration(
        team_id=team.id,
        min_team_member_count=2,
    )

    db.session.add(player_team)
    db.session.add(logs_tf_integration)

    auth_session = AuthSession(
        player_id=player.steam_id,
        key="test_key",
    )

    db.session.add(auth_session)

    event = Event(
        team_id=team.id,
        name="Test event",
        description="Test description",
        start_time=datetime.datetime.now(datetime.timezone.utc),
    )

    db.session.add(event)
    db.session.flush()

    player_event = PlayerEvent(
        event_id=event.id,
        player_id=76561198248436608,
        player_team_role_id=1,
    )

    ptr = PlayerTeamRole(
        player_team_id=player_team.id,
        role=PlayerTeamRole.Role.PocketSoldier,
        is_main=True,
    )

    db.session.add(player_event)
    db.session.add(ptr)

    db.session.commit()

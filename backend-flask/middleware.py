from functools import wraps
from flask import abort, make_response, request
from app_db import db
from models.auth_session import AuthSession
from models.player import Player
from models.player_team import PlayerTeam


def requires_authentication(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        auth = request.cookies.get("auth")

        if not auth:
            abort(401)

        statement = db.select(AuthSession).filter_by(key=auth)
        auth_session: AuthSession | None = \
            db.session.execute(statement).scalar_one_or_none()

        if not auth_session:
            abort(make_response({
                "error": "Invalid auth token"
            }, 401))
        player = auth_session.player
        kwargs["player"] = player
        kwargs["auth_session"] = auth_session
        return f(*args, **kwargs)
    return decorator

def requires_team_membership(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        player: Player | None = kwargs["player"]
        team_id: int = kwargs["team_id"]

        if not player:
            abort(401)

        player_team = db.session.query(
            PlayerTeam
        ).where(
            PlayerTeam.player == player
        ).where(
            PlayerTeam.team_id == team_id
        ).one_or_none()

        if not player_team:
            abort(404, "Player is not a member of this team")

        kwargs["player_team"] = player_team
        return f(*args, **kwargs)
    return decorator

def assert_team_authority(
    player_team: PlayerTeam,
    target_player_team: PlayerTeam | None = None,
    allow_self_target: bool = False
):
    if not player_team.is_team_leader:
        if not allow_self_target or player_team != target_player_team:
            abort(403)

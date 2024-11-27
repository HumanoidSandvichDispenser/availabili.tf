from functools import wraps
from typing import Optional
from flask import abort, make_response, request
from sqlalchemy.sql.operators import json_path_getitem_op
from app_db import db
from models.auth_session import AuthSession
from models.player import Player
from models.player_team import PlayerTeam
from models.team import Team


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

def requires_team_membership(
    path_param: Optional[str] = None,
    json_param: Optional[str] = None,
    query_param: Optional[str] = None
):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            player: Player | None = kwargs["player"]

            team_id: int
            if path_param:
                team_id = kwargs[path_param]
            elif json_param:
                team_id = getattr(kwargs["json"], json_param)
            elif query_param:
                team_id = getattr(kwargs["query"], query_param)
            else:
                team_id = kwargs["team_id"]

            if not player:
                abort(401)

            if not team_id:
                abort(500)

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
    return wrapper

def assert_team_membership(player: Player, team: Team):
    player_team = db.session.query(
        PlayerTeam
    ).where(
        PlayerTeam.player == player
    ).where(
        PlayerTeam.team == team
    ).one_or_none()

    if not player_team:
        abort(404)

    return player_team

def assert_team_authority(
    player_team: PlayerTeam,
    target_player_team: PlayerTeam | None = None,
    allow_self_target: bool = False
):
    if not player_team.is_team_leader:
        if not allow_self_target or player_team != target_player_team:
            abort(403)

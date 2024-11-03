import datetime
from typing import List
from flask import Blueprint, abort, jsonify, make_response, request
import pydantic
from flask_pydantic import validate
from spectree import Response
from models import Player, PlayerTeam, Team, TeamSpec, db
from middleware import requires_authentication
import models
from spec import spec, BaseModel


api_team = Blueprint("team", __name__, url_prefix="/team")

class CreateTeamJson(BaseModel):
    team_name: str
    webhook_url: str
    timezone: str

class ViewTeamResponse(BaseModel):
    team: models.TeamSpec

class ViewTeamsResponse(BaseModel):
    teams: list[models.TeamSpec]

@api_team.get("/all/")
@spec.validate(
    resp=Response(
        HTTP_200=ViewTeamsResponse,
        HTTP_403=None,
        HTTP_404=None,
    )
)
@requires_authentication
def view_teams(**kwargs):
    player: Player = kwargs["player"]
    response = fetch_teams_for_player(player, None)
    if isinstance(response, ViewTeamsResponse):
        return jsonify(response.dict())
    abort(404)

@api_team.get("/id/<team_id>/")
@spec.validate(
    resp=Response(
        HTTP_200=ViewTeamResponse,
        HTTP_403=None,
        HTTP_404=None,
    )
)
@requires_authentication
def view_team(team_id: int, **kwargs):
    player: Player = kwargs["player"]
    response = fetch_teams_for_player(player, team_id)
    if isinstance(response, ViewTeamResponse):
        return jsonify(response.dict())
    abort(404)

def fetch_teams_for_player(player: Player, team_id: int | None):
    q = db.session.query(
        Team
    ).join(
        PlayerTeam
    ).join(
        Player
    ).where(
        PlayerTeam.player_id == player.steam_id
    )

    if team_id is not None:
        q = q.where(PlayerTeam.team_id == team_id)

    def map_team_to_spec(team: Team) -> TeamSpec:
        return TeamSpec(
            id=team.id,
            team_name=team.team_name,
            discord_webhook_url=None
        )

    if team_id is None:
        teams = q.all()
        return ViewTeamsResponse(
            teams=list(map(map_team_to_spec, teams))
        )
    else:
        team = q.one_or_none()
        if team:
            return ViewTeamResponse(
                team=map_team_to_spec(team)
            )

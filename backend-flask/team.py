import datetime
from typing import List
from flask import Blueprint, jsonify, request
import pydantic
from flask_pydantic import validate
from models import Player, PlayerTeam, Team, db
from middleware import requires_authentication
import models


api_team = Blueprint("team", __name__, url_prefix="/team")

@api_team.get("/view/")
@api_team.get("/view/<team_id>/")
@requires_authentication
def view(team_id = None, **kwargs):
    player: Player = kwargs["player"]

    q_filter = PlayerTeam.player_id == player.steam_id
    if team_id is not None:
        q_filter = q_filter & (PlayerTeam.team_id == team_id)

    q = db.session.query(
        Team
    ).join(
        PlayerTeam
    ).join(
        Player
    ).filter(
        PlayerTeam.player_id == player.steam_id
    )

    def map_player_team_to_player_json(player_team: PlayerTeam):
        return {
            "steamId": player_team.player.steam_id,
            "username": player_team.player.username,
        }

    def map_team_to_json(team: Team):
        return {
            "teamName": team.team_name,
            "id": team.id,
            "players": list(map(map_player_team_to_player_json, team.players)),
        }

    if team_id is None:
        teams = q.all()
        return jsonify(list(map(map_team_to_json, teams)))
    else:
        team = q.one_or_none()
        if team:
            return jsonify(map_team_to_json(team))
        return jsonify(), 404

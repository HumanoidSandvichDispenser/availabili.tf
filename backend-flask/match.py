from flask import Blueprint, abort
from pydantic.v1 import validator
#from pydantic.functional_validators import field_validator
from spectree import Response
from sqlalchemy.orm import joinedload
from jobs.fetch_logstf import load_specific_match
from models.player_team import PlayerTeam
from models.team import Team
from models.team_match import TeamMatch, TeamMatchSchema
from spec import BaseModel, spec
from middleware import requires_authentication, requires_team_membership
from models.match import Match, MatchSchema
from app_db import db
from models.player import Player
from models.player_match import PlayerMatch


api_match = Blueprint("match", __name__, url_prefix="/match")

@api_match.get("/id/<int:match_id>")
@spec.validate(
    resp=Response(
        HTTP_200=MatchSchema,
    ),
    
)
@requires_authentication
def get_match(player: Player, match_id: int, **_):
    match = (
        db.session.query(Match)
        .join(PlayerMatch)
        .where(Match.logs_tf_id == match_id)
        .where(PlayerMatch.player_id == player.steam_id)
        .first()
    )

    if not match:
        abort(404)

    return MatchSchema.from_model(match).dict(by_alias=True), 200

class SubmitMatchJson(BaseModel):
    match_ids: list[int]

    @validator("match_ids")
    @classmethod
    def validate_match_ids(cls, match_ids):
        if len(match_ids) < 1:
            raise ValueError("match_ids must contain at least one match id")
        if len(match_ids) > 10:
            raise ValueError("match_ids must contain at most 10 match ids")

@api_match.put("/")
@spec.validate(
    resp=Response(
        HTTP_204=None,
    ),
    operation_id="submit_match",
)
@requires_authentication
def submit_match(json: SubmitMatchJson, **_):
    import sys
    print(json, file=sys.stderr)
    if json.match_ids is None:
        print("json.match_ids is None", file=sys.stderr)

    for id in json.match_ids:
        load_specific_match.delay(id, None)
    return { }, 204

@api_match.get("/team/<int:team_id>")
@spec.validate(
    resp=Response(
        HTTP_200=list[TeamMatchSchema],
    ),
    operation_id="get_matches_for_team",
)
@requires_authentication
@requires_team_membership()
def get_matches_for_team(team_id: Team, **_):
    matches = (
        db.session.query(TeamMatch)
        .where(TeamMatch.team_id == team_id)
        .options(joinedload(TeamMatch.match))
        .all()
    )

    return [TeamMatchSchema.from_model(match).dict(by_alias=True) for match in matches], 200

@api_match.get("/player")
@spec.validate(
    resp=Response(
        HTTP_200=list[TeamMatchSchema],
    ),
    operation_id="get_matches_for_player_teams",
)
@requires_authentication
def get_matches_for_player_teams(player: Player, **_):
    matches = (
        db.session.query(TeamMatch)
        .join(PlayerTeam, PlayerTeam.team_id == TeamMatch.team_id)
        .join(Match)
        .join(PlayerMatch)
        .where(PlayerMatch.player_id == player.steam_id)
        .options(joinedload(TeamMatch.match))
        .all()
    )
    return [TeamMatchSchema.from_model(match).dict(by_alias=True) for match in matches], 200

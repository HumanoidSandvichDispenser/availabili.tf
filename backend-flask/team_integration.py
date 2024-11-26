from flask import Blueprint
from spectree import Response
from sqlalchemy.orm import joinedload
from middleware import assert_team_authority, requires_authentication, requires_team_membership
from models.player_team import PlayerTeam
from models.team import Team
from models.team_integration import TeamIntegrationSchema
from spec import spec
from app_db import db


api_team_integration = Blueprint("team_integration", __name__)

@api_team_integration.get("/id/<team_id>/integrations")
@spec.validate(
    resp=Response(
        HTTP_200=TeamIntegrationSchema,
    ),
    operation_id="get_integrations"
)
@requires_authentication
@requires_team_membership()
def get_integrations(player_team: PlayerTeam, **_):
    team = db.session.query(
        Team
    ).where(
        Team.id == player_team.team_id
    ).options(
        joinedload(Team.discord_integration),
        joinedload(Team.logs_tf_integration),
    ).one()

    return team.get_integrations().dict(by_alias=True)

@api_team_integration.put("/id/<team_id>/integrations")
@spec.validate(
    resp=Response(
        HTTP_200=TeamIntegrationSchema,
    ),
    operation_id="update_integrations"
)
@requires_authentication
@requires_team_membership()
def update_integrations(
    player_team: PlayerTeam,
    json: TeamIntegrationSchema,
    **_
):
    assert_team_authority(player_team)
    team = db.session.query(
        Team
    ).where(
        Team.id == player_team.team_id
    ).options(
        joinedload(Team.discord_integration),
        joinedload(Team.logs_tf_integration),
    ).one()
    team.update_integrations(json)
    db.session.commit()
    return json.dict(by_alias=True)

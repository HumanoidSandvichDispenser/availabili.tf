from flask import Blueprint, abort, make_response
from spectree import Response
from typing import cast


from app_db import db
from middleware import assert_team_authority, requires_authentication, requires_team_membership
from models.player import Player
from models.player_team import PlayerTeam
from models.team_integration import AbstractTeamIntegrationSchema, TeamDiscordIntegration, TeamIntegration, TeamIntegrationSchema
from spec import spec


api_team_integration = Blueprint("team_integration", __name__)

@api_team_integration.get("/id/<team_id>/integrations")
@spec.validate(
    resp=Response(
        HTTP_200=list[TeamIntegrationSchema],
        HTTP_404=None,
    ),
    operation_id="get_integrations"
)
@requires_authentication
def get_integrations(player: Player, team_id: int, **_):
    player_team = db.session.query(
        PlayerTeam
    ).where(
        PlayerTeam.player_id == player.steam_id
    ).where(
        PlayerTeam.team_id == team_id
    ).one_or_none()

    if not player_team:
        abort(404)

    integrations = db.session.query(
        TeamIntegration
    ).where(
        TeamIntegration.team_id == team_id
    ).all()

    def map_integration_to_schema(integration: TeamIntegration):
        return TeamIntegrationSchema.from_model(
            integration
        ).dict(by_alias=True)

    return list(map(map_integration_to_schema, integrations))

@api_team_integration.post("/id/<team_id>/integrations/<integration_type>")
@spec.validate(
    resp=Response(
        HTTP_200=TeamIntegrationSchema,
    ),
    operation_id="create_integration"
)
@requires_authentication
@requires_team_membership
def create_integration(player_team: PlayerTeam, integration_type: str, **_):
    assert_team_authority(player_team)

    if integration_type == "discord":
        integration = TeamDiscordIntegration()
        integration.team_id = player_team.team_id
        integration.webhook_url = ""
    else:
        abort(404)

    db.session.add(integration)
    db.session.commit()

    return TeamIntegrationSchema.from_model(
        integration
    ).dict(by_alias=True), 200

@api_team_integration.delete("/id/<team_id>/integrations/<integration_id>")
@spec.validate(
    resp=Response(
        HTTP_204=None,
    ),
    operation_id="delete_integration"
)
@requires_authentication
@requires_team_membership
def delete_integration(player_team: PlayerTeam, integration_id: int, **_):
    assert_team_authority(player_team)

    integration = db.session.query(
        TeamIntegration
    ).where(
        TeamIntegration.team_id == player_team.team_id
    ).where(
        TeamIntegration.id == integration_id
    ).one_or_none()

    if not integration:
        abort(404)

    db.session.delete(integration)
    db.session.commit()

    return make_response({ }, 204)

@api_team_integration.patch("/id/<team_id>/integrations/<integration_id>")
@spec.validate(
    resp=Response(
        HTTP_200=TeamIntegrationSchema,
    ),
    operation_id="update_integration"
)
@requires_authentication
@requires_team_membership
def update_integration(
    player_team: PlayerTeam,
    integration_id: int,
    json: AbstractTeamIntegrationSchema,
    **_
):
    assert_team_authority(player_team)

    integration = db.session.query(
        TeamIntegration
    ).where(
        TeamIntegration.team_id == player_team.team_id
    ).where(
        TeamIntegration.id == integration_id
    ).one_or_none()

    if not integration:
        abort(404)

    if isinstance(integration, TeamDiscordIntegration):
        if json.__root__.integration_type == "team_discord_integrations":
            discord_integration = cast(TeamDiscordIntegration, json.__root__)
            integration.webhook_url = discord_integration.webhook_url
        else:
            abort(400)
    else:
        abort(404)

    db.session.commit()

    return TeamIntegrationSchema.from_model(
        integration
    ).dict(by_alias=True), 200

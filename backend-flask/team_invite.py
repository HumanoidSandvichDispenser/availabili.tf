from random import randint
from flask import Blueprint, abort, make_response
from spectree import Response
import time

from app_db import db
from middleware import requires_authentication, requires_team_membership
from models.player import Player
from models.player_team import PlayerTeam
from models.team_invite import TeamInvite, TeamInviteSchema
from spec import BaseModel, spec


api_team_invite = Blueprint("team_invite", __name__)

@api_team_invite.get("/id/<team_id>/invite")
@spec.validate(
    resp=Response(
        HTTP_200=list[TeamInviteSchema],
        HTTP_404=None,
    ),
    operation_id="get_invites"
)
@requires_authentication
@requires_team_membership()
def get_invites(team_id: int, **_):
    invites = db.session.query(
        TeamInvite
    ).where(
        TeamInvite.team_id == team_id
    ).all()

    def map_invite_to_schema(invite: TeamInvite):
        return TeamInviteSchema(
            key=invite.key,
            team_id=invite.team_id,
            created_at=invite.created_at,
        ).dict(by_alias=True)

    return list(map(map_invite_to_schema, invites)), 200

@api_team_invite.post("/id/<team_id>/invite")
@spec.validate(
    resp=Response(
        HTTP_200=TeamInviteSchema,
        HTTP_404=None,
    ),
    operation_id="create_invite"
)
@requires_authentication
@requires_team_membership()
def create_invite(team_id: int, **_):
    team_id_shifted = int(team_id) << 48
    random_value_shifted = int(randint(0, (1 << 16) - 1)) << 32
    timestamp = int(time.time()) & ((1 << 32) - 1)

    key_int = timestamp | team_id_shifted | random_value_shifted
    key_hex = "%0.16X" % key_int

    invite = TeamInvite()
    invite.team_id = team_id
    invite.key = key_hex

    db.session.add(invite)
    db.session.flush()
    db.session.refresh(invite)

    response = TeamInviteSchema(
        key=key_hex,
        team_id=team_id,
        created_at=invite.created_at
    )

    db.session.commit()

    return response.dict(by_alias=True), 200

class ConsumeInviteResponse(BaseModel):
    team_id: int

@api_team_invite.post("/consume-invite/<key>")
@spec.validate(
    resp=Response(
        HTTP_200=ConsumeInviteResponse,
        HTTP_404=None,
    ),
    operation_id="consume_invite"
)
@requires_authentication
def consume_invite(player: Player, key: str, **_):
    invite = db.session.query(
        TeamInvite
    ).where(
        TeamInvite.key == key
    ).one_or_none()


    if not invite:
        abort(404)

    team_id = invite.team_id

    player_team = db.session.query(
        PlayerTeam
    ).where(
        PlayerTeam.player_id == player.steam_id
    ).where(
        PlayerTeam.team_id == team_id
    ).one_or_none()

    if player_team:
        abort(409)

    player_team = PlayerTeam()
    player_team.player = player
    player_team.team_id = team_id

    db.session.add(player_team)

    if invite.delete_on_use:
        db.session.delete(invite)

    db.session.commit()

    return ConsumeInviteResponse(team_id=team_id).dict(by_alias=True), 200

@api_team_invite.delete("/id/<team_id>/invite/<key>")
@spec.validate(
    resp=Response(
        HTTP_204=None,
        HTTP_404=None,
    ),
    operation_id="revoke_invite"
)
@requires_authentication
def revoke_invite(player: Player, team_id: int, key: str, **_):
    player_team = db.session.query(
        PlayerTeam
    ).where(
        PlayerTeam.player_id == player.steam_id
    ).where(
        PlayerTeam.team_id == team_id
    ).one_or_none()

    if not player_team:
        abort(404)

    invite = db.session.query(
        TeamInvite
    ).where(
        TeamInvite.team_id == team_id
    ).where(
        TeamInvite.key == key
    ).one_or_none()

    if not invite:
        abort(404)

    db.session.delete(invite)
    db.session.commit()
    return make_response({ }, 204)


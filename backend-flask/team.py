from datetime import datetime, timezone
from random import randint, random
import sys
import time
from typing import List
from flask import Blueprint, abort, jsonify, make_response, request
from pydantic.v1 import validator
from spectree import Response
from sqlalchemy.orm import joinedload, subqueryload
from models import Player, PlayerSchema, PlayerTeam, PlayerTeamAvailability, PlayerTeamRole, PlayerTeamSchema, Team, TeamInvite, TeamInviteSchema, TeamSchema, db
from middleware import requires_authentication
import models
from spec import spec, BaseModel
import pytz


api_team = Blueprint("team", __name__, url_prefix="/team")

def map_team_to_schema(team: Team):
    return TeamSchema(
        id=team.id,
        team_name=team.team_name,
        discord_webhook_url=None,
        tz_timezone=team.tz_timezone,
        minute_offset=team.minute_offset
    )

def map_player_to_schema(player: Player):
    return PlayerSchema(
        steam_id=str(player.steam_id),
        username=player.username,
    )

class CreateTeamJson(BaseModel):
    team_name: str
    discord_webhook_url: str | None = None
    league_timezone: str

    @validator("league_timezone")
    @classmethod
    def validate_timezone(cls, v):
        if v not in pytz.all_timezones:
            raise ValueError(v + " is not a valid timezone")
        return v

    @validator("team_name")
    @classmethod
    def validate_team_name(cls, v: str):
        if not v:
            raise ValueError("Team name can not be blank")
        return v

class ViewTeamResponse(BaseModel):
    team: models.TeamSchema

class ViewTeamsResponse(BaseModel):
    teams: list[models.TeamSchema]

@api_team.post("/")
@spec.validate(
    resp=Response(
        HTTP_200=ViewTeamResponse,
        HTTP_403=None,
    ),
    operation_id="create_team"
)
@requires_authentication
def create_team(json: CreateTeamJson, player: Player, **kwargs):
    team = Team(
        team_name=json.team_name,
        tz_timezone=json.league_timezone,
    )
    if json.discord_webhook_url:
        team.discord_webhook_url = json.discord_webhook_url

    db.session.add(team)
    db.session.flush()  # flush, so we can get autoincremented id

    player_team = PlayerTeam(
        player_id=player.steam_id,
        team_id=team.id,
        is_team_leader=True
     )
    db.session.add(player_team)

    db.session.commit()

    response = ViewTeamResponse(team=map_team_to_schema(team))
    return jsonify(response.dict(by_alias=True))

@api_team.delete("/id/<team_id>/")
@spec.validate(
    resp=Response(
        HTTP_200=None,
        HTTP_403=None,
        HTTP_404=None,
    ),
    operation_id="delete_team"
)
def delete_team(player: Player, team_id: int):
    player_team = db.session.query(
        PlayerTeam
    ).where(
        PlayerTeam.team_id == team_id
    ).where(
        PlayerTeam.player_id == player.steam_id
    ).one_or_none()

    if not player_team:
        abort(404)

    if not player_team.is_team_leader:
        abort(403)

    db.session.delete(player_team.team)
    db.session.commit()
    return make_response(200)

class AddPlayerJson(BaseModel):
    team_role: PlayerTeam.TeamRole = PlayerTeam.TeamRole.Player
    is_team_leader: bool = False

@api_team.put("/id/<team_id>/player/<player_id>/")
@spec.validate(
    resp=Response(
        HTTP_200=None,
        HTTP_403=None,
        HTTP_404=None,
    ),
    operation_id="create_or_update_player"
)
def add_player(player: Player, team_id: int, player_id: int, json: AddPlayerJson):
    player_team = db.session.query(
        PlayerTeam
    ).where(
        PlayerTeam.player_id == player.steam_id
    ).where(
        PlayerTeam.team_id == team_id
    ).one_or_none()

    if not player_team:
        abort(404)

    if not player_team.is_team_leader:
        abort(403)

    target_player_team = db.session.query(
        PlayerTeam
    ).where(
        PlayerTeam.player_id == player_id
    ).where(
        PlayerTeam.team_id == team_id
    ).one_or_none()

    if not target_player_team:
        target_player = db.session.query(
            Player
        ).where(
            Player.steam_id == player_id
        ).one_or_none()

        if not target_player:
            abort(404)

        target_player_team = PlayerTeam()
        target_player_team.player_id = player_id
        target_player_team.team_id = player_team.team_id

    target_player_team.team_role = json.team_role
    target_player_team.is_team_leader = json.is_team_leader

    db.session.commit()
    return make_response(200)

@api_team.get("/all/")
@spec.validate(
    resp=Response(
        HTTP_200=ViewTeamsResponse,
        HTTP_403=None,
        HTTP_404=None,
    ),
    operation_id="get_teams"
)
@requires_authentication
def view_teams(**kwargs):
    player: Player = kwargs["player"]
    response = fetch_teams_for_player(player, None)
    if isinstance(response, ViewTeamsResponse):
        return jsonify(response.dict(by_alias=True))
    abort(404)

@api_team.get("/id/<team_id>/")
@spec.validate(
    resp=Response(
        HTTP_200=ViewTeamResponse,
        HTTP_403=None,
        HTTP_404=None,
    ),
    operation_id="get_team"
)
@requires_authentication
def view_team(team_id: int, **kwargs):
    player: Player = kwargs["player"]
    response = fetch_teams_for_player(player, team_id)
    if isinstance(response, ViewTeamResponse):
        return jsonify(response.dict(by_alias=True))
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

    if team_id is None:
        teams = q.all()
        return ViewTeamsResponse(
            teams=list(map(map_team_to_schema, teams))
        )
    else:
        team = q.one_or_none()
        if team:
            return ViewTeamResponse(
                team=map_team_to_schema(team)
            )

class ViewTeamMembersResponse(PlayerSchema):
    class RoleSchema(BaseModel):
        role: str
        is_main: bool

    roles: list[RoleSchema]
    availability: int
    playtime: float
    created_at: datetime

@api_team.get("/id/<team_id>/players")
@spec.validate(
    resp=Response(
        HTTP_200=list[ViewTeamMembersResponse],
        HTTP_403=None,
        HTTP_404=None,
    ),
    operation_id="get_team_members"
)
@requires_authentication
def view_team_members(player: Player, team_id: int, **kwargs):
    now = datetime.now(timezone.utc)

    player_teams_query = db.session.query(
        PlayerTeam
    ).where(
        PlayerTeam.team_id == team_id
    ).options(
        # eager load so SQLAlchemy does not make a second query just to join
        joinedload(PlayerTeam.player),
        joinedload(PlayerTeam.player_roles),
        joinedload(PlayerTeam.availability.and_(
            (PlayerTeamAvailability.start_time <= now) &
                (PlayerTeamAvailability.end_time > now)
        )),
    )

    player_teams = player_teams_query.all()

    if not next(filter(lambda x: x.player_id == player.steam_id, player_teams)):
        abort(404)

    def map_role_to_schema(player_team_role: PlayerTeamRole):
        return ViewTeamMembersResponse.RoleSchema(
            role=player_team_role.role.name,
            is_main=player_team_role.is_main,
        )

    def map_to_response(player_team: PlayerTeam):
        roles = player_team.player_roles
        player = player_team.player

        availability = 0
        if len(player_team.availability) > 0:
            print(player_team.availability)
            availability = player_team.availability[0].availability

        return ViewTeamMembersResponse(
            username=player.username,
            steam_id=str(player.steam_id),
            roles=list(map(map_role_to_schema, roles)),
            availability=availability,
            playtime=player_team.playtime.total_seconds() / 3600,
            created_at=player_team.created_at,
        ).dict(by_alias=True)

    return list(map(map_to_response, player_teams))

class EditMemberRolesJson(BaseModel):
    roles: list[ViewTeamMembersResponse.RoleSchema]

@api_team.patch("/id/<team_id>/edit-player/<target_player_id>")
@spec.validate(
    resp=Response(
        HTTP_204=None,
        HTTP_403=None,
        HTTP_404=None,
    ),
    operation_id="edit_member_roles"
)
@requires_authentication
def edit_member_roles(
    json: EditMemberRolesJson,
    player: Player,
    team_id: int,
    target_player_id: int,
    **kwargs,
):
    target_player = db.session.query(
        PlayerTeam
    ).where(
        PlayerTeam.player_id == target_player_id
    ).where(
        PlayerTeam.team_id == team_id
    ).options(
        joinedload(PlayerTeam.player),
        joinedload(PlayerTeam.player_roles),
    ).one_or_none()

    if not target_player:
        abort(401)

    # TODO: change this to a MERGE statement

    for role in target_player.player_roles:
        # delete role if not found in json
        f = filter(lambda x: x.role == role.role.name, json.roles)
        matched_role = next(f, None)

        if not matched_role:
            db.session.delete(role)

    for schema in json.roles:
        role = PlayerTeamRole()
        role.player_team = target_player
        role.role = PlayerTeamRole.Role[schema.role]
        role.is_main = schema.is_main
        db.session.merge(role)

    db.session.commit()

    return make_response({ }, 204)

@api_team.get("/id/<team_id>/invite")
@spec.validate(
    resp=Response(
        HTTP_200=list[TeamInviteSchema],
        HTTP_404=None,
    ),
    operation_id="get_invites"
)
@requires_authentication
def get_invites(player: Player, team_id: int, **kwargs):
    player_team = db.session.query(
        PlayerTeam
    ).where(
        PlayerTeam.player_id == player.steam_id
    ).where(
        PlayerTeam.team_id == team_id
    ).one_or_none()

    if not player_team:
        abort(404)

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

@api_team.post("/id/<team_id>/invite")
@spec.validate(
    resp=Response(
        HTTP_200=TeamInviteSchema,
        HTTP_404=None,
    ),
    operation_id="create_invite"
)
@requires_authentication
def create_invite(player: Player, team_id: int, **kwargs):
    player_team = db.session.query(
        PlayerTeam
    ).where(
        PlayerTeam.player_id == player.steam_id
    ).where(
        PlayerTeam.team_id == team_id
    ).one_or_none()

    if not player_team:
        abort(404)

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

@api_team.post("/id/<team_id>/consume-invite/<key>")
@spec.validate(
    resp=Response(
        HTTP_204=None,
        HTTP_404=None,
    ),
    operation_id="consume_invite"
)
@requires_authentication
def consume_invite(player: Player, team_id: int, key: str, **kwargs):
    invite = db.session.query(
        TeamInvite
    ).where(
        TeamInvite.team_id == team_id
    ).where(
        TeamInvite.key == key
    ).one_or_none()

    if not invite:
        abort(404)

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

    return make_response({ }, 204)

@api_team.delete("/id/<team_id>/invite/<key>")
@spec.validate(
    resp=Response(
        HTTP_204=None,
        HTTP_404=None,
    ),
    operation_id="revoke_invite"
)
@requires_authentication
def revoke_invite(player: Player, team_id: int, key: str, **kwargs):
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

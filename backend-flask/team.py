from datetime import datetime, timedelta, timezone
from typing import cast
from flask import Blueprint, abort, make_response
from pydantic.v1 import validator
from spectree import Response
from sqlalchemy.orm import joinedload
from app_db import db
from models.player import Player, PlayerSchema
from models.player_team import PlayerTeam
from models.player_team_availability import PlayerTeamAvailability
from models.player_team_role import PlayerTeamRole, RoleSchema
from models.team import Team, TeamSchema
from middleware import requires_authentication
from spec import spec, BaseModel
from team_invite import api_team_invite
from team_integration import api_team_integration
import pytz


api_team = Blueprint("team", __name__, url_prefix="/team")
api_team.register_blueprint(api_team_invite)
api_team.register_blueprint(api_team_integration)

def map_player_to_schema(player: Player):
    return PlayerSchema(
        steam_id=str(player.steam_id),
        username=player.username,
    )

class CreateTeamJson(BaseModel):
    team_name: str
    discord_webhook_url: str | None = None
    minute_offset: int = 0
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
    team: TeamSchema

class ViewTeamsResponse(BaseModel):
    teams: list[TeamSchema]

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
        minute_offset=json.minute_offset,
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

    response = ViewTeamResponse(team=TeamSchema.from_model(team))
    return response.dict(by_alias=True), 200

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

@api_team.delete("/id/<team_id>/player/<target_player_id>/")
@spec.validate(
    resp=Response(
        HTTP_200=None,
        HTTP_403=None,
        HTTP_404=None,
    ),
    operation_id="remove_player_from_team"
)
@requires_authentication
def remove_player_from_team(player: Player, team_id: int, target_player_id: int, **kwargs):
    player_team = db.session.query(
        PlayerTeam
    ).where(
        PlayerTeam.team_id == team_id
    ).where(
        PlayerTeam.player_id == player.steam_id
    ).one_or_none()

    if not player_team:
        abort(404)

    target_player_team = db.session.query(
        PlayerTeam
    ).where(
        PlayerTeam.team_id == team_id
    ).where(
        PlayerTeam.player_id == target_player_id
    ).one_or_none()

    if not target_player_team:
        abort(404)

    is_team_leader = player_team.is_team_leader

    if not is_team_leader and player_team != target_player_team:
        abort(403)

    team = target_player_team.team

    db.session.delete(target_player_team)
    db.session.refresh(team)

    if len(team.players) == 0:
        # delete the team if the only member
        db.session.delete(team)
    else:
        # if there doesn't exist another team leader, promote the first player
        team_leaders = db.session.query(
            PlayerTeam
        ).where(
            PlayerTeam.team_id == team_id
        ).where(
            PlayerTeam.is_team_leader == True
        ).all()

        if len(team_leaders) == 0:
            team.players[0].is_team_leader = True

    db.session.commit()

    return make_response({ }, 200)

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
        return response.dict(by_alias=True)
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
        return response.dict(by_alias=True)
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
            teams=list(map(TeamSchema.from_model, teams))
        )
    else:
        team = q.one_or_none()
        if team:
            return ViewTeamResponse(
                team=TeamSchema.from_model(team)
            )

class ViewTeamMembersResponse(PlayerSchema):
    roles: list[RoleSchema]
    availability: list[int]
    playtime: float
    created_at: datetime
    is_team_leader: bool = False

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
    next_hour = now + timedelta(hours=1)

    player_teams_query = db.session.query(
        PlayerTeam
    ).where(
        PlayerTeam.team_id == team_id
    ).options(
        # eager load so SQLAlchemy does not make a second query just to join
        joinedload(PlayerTeam.player),
        joinedload(PlayerTeam.player_roles),
        joinedload(PlayerTeam.availability.and_(
            (PlayerTeamAvailability.start_time <= next_hour) &
                (PlayerTeamAvailability.end_time > now)
        )),
    )

    player_teams = player_teams_query.all()

    if not next(filter(lambda x: x.player_id == player.steam_id, player_teams)):
        abort(404)

    def map_role_to_schema(player_team_role: PlayerTeamRole):
        return RoleSchema(
            role=player_team_role.role.name,
            is_main=player_team_role.is_main,
        )

    def map_to_response(player_team: PlayerTeam):
        roles = player_team.player_roles
        player = player_team.player

        availability = [0, 0]

        for record in player_team.availability:
            if record.start_time <= now < record.end_time:
                availability[0] = record.availability
            if record.start_time <= next_hour < record.end_time:
                availability[1] = record.availability

        return ViewTeamMembersResponse(
            username=player.username,
            steam_id=str(player.steam_id),
            roles=list(map(map_role_to_schema, roles)),
            availability=availability,
            playtime=player_team.playtime.total_seconds() / 3600,
            created_at=player_team.created_at,
            is_team_leader=player_team.is_team_leader,
        ).dict(by_alias=True)

    return list(map(map_to_response, player_teams))

class EditMemberRolesJson(BaseModel):
    roles: list[RoleSchema]

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

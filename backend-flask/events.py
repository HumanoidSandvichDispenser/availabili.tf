#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2024 sandvich <sandvich@archtop>
#
# Distributed under terms of the MIT license.


from datetime import datetime

from flask import Blueprint, abort, make_response
from spectree import Response
from sqlalchemy.sql import tuple_
from models.player import Player
from models.player_event import PlayerEvent, PlayerEventRolesSchema
from models.player_team_availability import PlayerTeamAvailability
from models.player_team_role import PlayerRoleSchema, PlayerTeamRole
from models.team import Team
from spec import BaseModel, spec
from middleware import assert_team_authority, assert_team_membership, requires_authentication, requires_team_membership
from models.event import Event, EventSchema
from models.player_team import PlayerTeam
from app_db import db


api_events = Blueprint("events", __name__, url_prefix="/events")

@api_events.get("/<int:event_id>")
@spec.validate(
    resp=Response(
        HTTP_200=EventSchema,
    ),
    operation_id="get_event",
)
def get_event(event_id: int):
    event = db.session.query(Event).filter(Event.id == event_id).one_or_none()

    if not event:
        abort(404)

    return EventSchema.from_model(event).dict(by_alias=True)

@api_events.get("/team/id/<int:team_id>")
@spec.validate(
    resp=Response(
        HTTP_200=list[EventSchema],
    ),
    operation_id="get_team_events",
)
def get_team_events(team_id: int):
    events = db.session.query(
        Event
    ).filter(
        Event.team_id == team_id
    ).order_by(
        Event.start_time
    ).all()

    def map_to_schema(event: Event):
        return EventSchema.from_model(event).dict(by_alias=True)

    return list(map(map_to_schema, events))

@api_events.get("/user/id/<int:user_id>")
def get_user_events(user_id: int):
    raise NotImplementedError()

class CreateEventJson(BaseModel):
    name: str
    description: str
    start_time: datetime
    player_roles: list[PlayerRoleSchema]

@api_events.post("/team/id/<int:team_id>")
@spec.validate(
    resp=Response(
        HTTP_200=EventSchema,
    ),
    operation_id="create_event",
)
@requires_authentication
@requires_team_membership()
def create_event(player_team: PlayerTeam, team_id: int, json: CreateEventJson, **_):
    event = Event()
    event.team_id = player_team.team_id
    event.name = json.name
    event.description = json.description
    event.start_time = json.start_time

    db.session.add(event)
    db.session.flush()
    db.session.refresh(event)

    tuples = map(lambda x: (x.player.steam_id, x.role.role), json.player_roles)

    results = db.session.query(
        PlayerTeam, PlayerTeamRole.id, PlayerTeamAvailability.availability
    ).join(
        PlayerTeamRole
    ).outerjoin(
        PlayerTeamAvailability,
        (PlayerTeamAvailability.player_team_id == PlayerTeam.id) &
        (PlayerTeamAvailability.start_time <= event.start_time) &
            (PlayerTeamAvailability.end_time > event.start_time)
    ).where(
        PlayerTeam.team_id == team_id
    ).where(
        # (player_id, role) in (...)
        tuple_(PlayerTeam.player_id, PlayerTeamRole.role).in_(tuples)
    ).all()

    for player_team, role_id, availability in map(lambda x: x.tuple(), results):
        player_event = PlayerEvent()
        player_event.player_id = player_team.player_id
        player_event.event_id = event.id
        player_event.player_team_role_id = role_id

        # autoconfirm if availability = 2
        player_event.has_confirmed = (availability == 2)

        db.session.add(player_event)

    db.session.commit()

    event.update_discord_message()

    return EventSchema.from_model(event).dict(by_alias=True), 200

@api_events.put("/<int:event_id>/attendance")
@spec.validate(
    resp=Response(
        HTTP_204=None,
    )
)
@requires_authentication
@requires_team_membership()
def attend_event(player_team: PlayerTeam, event_id: int, **_):
    player_event = db.session.query(
        PlayerEvent
    ).where(
        PlayerEvent.event_id == event_id
    ).where(
        PlayerEvent.player_id == player_team.player_id
    ).join(
        Event
    ).where(
        Event.team_id == player_team.team_id
    ).one_or_none()

    if not player_event:
        player_event = PlayerEvent()
        player_event.event_id = event_id
        player_event.player_id = player_team.player_id
        db.session.add(player_event)

    player_event.has_confirmed = True

    db.session.commit()

    player_event.event.update_discord_message()

    return make_response({ }, 204)

@api_events.delete("/<int:event_id>/attendance")
@spec.validate(
    resp=Response(
        HTTP_204=None,
    )
)
@requires_authentication
@requires_team_membership()
def unattend_event(player_team: PlayerTeam, event_id: int, **_):
    result = db.session.query(
        PlayerEvent, Event
    ).where(
        PlayerEvent.event_id == event_id
    ).where(
        PlayerEvent.player_id == player_team.player_id
    ).join(
        Event
    ).where(
        Event.team_id == player_team.team_id
    ).one_or_none()

    if not result:
        abort(404)

    player_event, event = result.tuple()

    db.session.delete(player_event)
    db.session.commit()

    event.update_discord_message()

    return make_response({ }, 204)

class GetEventPlayersResponse(BaseModel):
    players: list[PlayerEventRolesSchema]

@api_events.get("/<int:event_id>/players")
@spec.validate(
    resp=Response(
        HTTP_200=GetEventPlayersResponse,
    ),
    operation_id="get_event_players",
)
@requires_authentication
def get_event_players(player: Player, event_id: int, **_):
    event = db.session.query(Event).where(Event.id == event_id).one_or_none()
    if not event:
        abort(404)
    assert_team_membership(player, event.team)

    players_events = db.session.query(
        PlayerEvent
    ).join(
        Event,
        Event.id == PlayerEvent.event_id
    ).join(
        PlayerTeam,
        PlayerTeam.team_id == Event.team_id & PlayerEvent.player_id == PlayerTeam.player_id
    ).where(
        PlayerEvent.event_id == event_id
    ).all()

    player_event_roles = [
        PlayerEventRolesSchema.from_event_player_team(
            player_event, player_event.player_team
        )
        for player_event in players_events
    ]

    return GetEventPlayersResponse(
        players=player_event_roles
    ).dict(by_alias=True), 200

@api_events.patch("/<int:event_id>/players")
@requires_authentication
@requires_team_membership()
def set_event_players(player_team: PlayerTeam, event_id: int, **_):
    assert_team_authority(player_team, None)

    # merge players into event
    db.session.query(Event).filter(Event.id == event_id).update({"players": []})

    raise NotImplementedError()

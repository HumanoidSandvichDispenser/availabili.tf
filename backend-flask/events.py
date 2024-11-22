#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2024 sandvich <sandvich@archtop>
#
# Distributed under terms of the MIT license.


from datetime import datetime

from flask import Blueprint, abort
from spectree import Response
from models.player_event import PlayerEvent
from models.player import Player
from spec import BaseModel, spec
from middleware import assert_team_authority, requires_authentication, requires_team_membership
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
    player_ids: list[int]

@api_events.post("/team/id/<int:team_id>")
@spec.validate(
    resp=Response(
        HTTP_200=EventSchema,
    )
)
@requires_authentication
@requires_team_membership()
def create_event(player_team: PlayerTeam, json: CreateEventJson, **_):
    event = Event()
    event.team_id = player_team.team_id
    event.name = json.name
    event.description = json.description
    event.start_time = json.start_time

    db.session.add(event)
    db.session.flush()
    db.session.refresh(event)

    players_teams = db.session.query(
        PlayerTeam
    ).join(
        Player
    ).where(
        PlayerTeam.team_id == player_team.team_id
    ).where(
        PlayerTeam.player_id.in_(json.player_ids)
    ).all()

    for player_team in players_teams:
        player = player_team.player
        player_event = PlayerEvent()
        player_event.player_id = player.steam_id
        player_event.event_id = event.id
        db.session.add(player_event)

    db.session.commit()

    return EventSchema.from_model(event).dict(by_alias=True), 200

@api_events.patch("/<int:event_id>/players")
@requires_authentication
@requires_team_membership()
def set_event_players(player_team: PlayerTeam, event_id: int, **_):
    assert_team_authority(player_team, None)

    # merge players into event
    db.session.query(Event).filter(Event.id == event_id).update({"players": []})

    raise NotImplementedError()

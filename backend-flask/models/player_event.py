from typing import Optional
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.types import Boolean
import app_db
import spec


class PlayerEvent(app_db.BaseModel):
    __tablename__ = "players_events"

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.steam_id"), primary_key=True)
    player_team_role_id: Mapped[int] = mapped_column(ForeignKey("players_teams_roles.id"), nullable=True)
    has_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)

    event: Mapped["Event"] = relationship("Event", back_populates="players")
    player: Mapped["Player"] = relationship("Player", back_populates="events")
    player_team: Mapped["PlayerTeam"] = relationship(
        "PlayerTeam",
        secondary="players",
        primaryjoin="PlayerEvent.player_id == Player.steam_id",
        secondaryjoin="PlayerTeam.player_id == Player.steam_id",
        viewonly=True,
    )
    role: Mapped["PlayerTeamRole"] = relationship("PlayerTeamRole")

class EventWithPlayerSchema(spec.BaseModel):
    event: "EventSchema"
    player_event: Optional["PlayerEventRolesSchema"]

    @classmethod
    def from_event_player_event(cls, event: "Event", player_event: Optional["PlayerEvent"]):
        res = cls(
            event=EventSchema.from_model(event),
            player_event=None,
        )

        if player_event:
            res.player_event = PlayerEventRolesSchema.from_event_player_team(
                player_event, player_event.player_team
            )

        return res

class PlayerEventRolesSchema(spec.BaseModel):
    player: "PlayerSchema"
    role: Optional["RoleSchema"]
    roles: list["RoleSchema"]
    has_confirmed: bool
    playtime: int

    @classmethod
    def from_event_player_team(cls, player_event: "PlayerEvent", player_team: "PlayerTeam"):
        return cls(
            player=PlayerSchema.from_model(player_event.player),
            role=RoleSchema.from_model(player_event.role) if player_event.role else None,
            roles=[RoleSchema.from_model(role) for role in player_team.player_roles],
            has_confirmed=player_event.has_confirmed,
            playtime=int(player_team.playtime.total_seconds()),
        )


from models.event import Event, EventSchema
from models.player import Player, PlayerSchema
from models.player_team_role import PlayerTeamRole, RoleSchema
from models.player_team import PlayerTeam

from datetime import datetime, timedelta
import enum
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP, Boolean, Enum, Integer, Interval
import app_db
import spec


class PlayerTeam(app_db.BaseModel):
    __tablename__ = "players_teams"

    class TeamRole(enum.Enum):
        Player = 0
        CoachMentor = 1

    # surrogate key
    id: Mapped[int] = mapped_column(
        Integer,
        autoincrement=True,
        primary_key=True,
    )

    # primary key
    player_id: Mapped[int] = mapped_column(ForeignKey("players.steam_id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    player: Mapped["Player"] = relationship(back_populates="teams")
    team: Mapped["Team"] = relationship(back_populates="players")

    player_roles: Mapped[list["PlayerTeamRole"]] = relationship("PlayerTeamRole", back_populates="player_team")
    availability: Mapped[list["PlayerTeamAvailability"]] = relationship(back_populates="player_team")

    team_role: Mapped[TeamRole] = mapped_column(Enum(TeamRole), default=TeamRole.Player)
    playtime: Mapped[timedelta] = mapped_column(Interval, default=timedelta(0))
    is_team_leader: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

class PlayerTeamSchema(spec.BaseModel):
    player: "PlayerSchema"
    team: "TeamSchema"


from models.player import Player, PlayerSchema
from models.player_team_availability import PlayerTeamAvailability
from models.player_team_role import PlayerTeamRole
from models.team import Team, TeamSchema

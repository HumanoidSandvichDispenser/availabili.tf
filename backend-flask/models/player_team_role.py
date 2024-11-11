import enum

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.types import Boolean, Enum
import app_db


class PlayerTeamRole(app_db.BaseModel):
    __tablename__ = "players_teams_roles"

    class Role(enum.Enum):
        Unknown = 0

        Scout = 1
        PocketScout = 2
        FlankScout = 3

        Soldier = 4
        PocketSoldier = 5
        Roamer = 6

        Pyro = 7
        Demoman = 8
        HeavyWeapons = 9
        Engineer = 10
        Medic = 11
        Sniper = 12
        Spy = 13

    player_id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(primary_key=True)

    player_team: Mapped["PlayerTeam"] = relationship("PlayerTeam", back_populates="player_roles")

    #player: Mapped["Player"] = relationship(back_populates="teams")

    role: Mapped[Role] = mapped_column(Enum(Role), primary_key=True)
    is_main: Mapped[bool] = mapped_column(Boolean)

    from models.player_team import PlayerTeam

    __table_args__ = (
        ForeignKeyConstraint(
            [player_id, team_id],
            [PlayerTeam.player_id, PlayerTeam.team_id]
        ),
    )

import enum

from sqlalchemy.orm.properties import ForeignKey

import spec
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.types import BigInteger, Boolean, Enum, Integer
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

    # surrogate key
    id: Mapped[int] = mapped_column(
        Integer,
        autoincrement=True,
        primary_key=True,
    )

    # primary key
    player_team_id = mapped_column(ForeignKey("players_teams.id"), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)

    player_team: Mapped["PlayerTeam"] = relationship(
        "PlayerTeam",
        back_populates="player_roles"
    )

    is_main: Mapped[bool] = mapped_column(Boolean)

    __table_args__ = (
        UniqueConstraint("player_team_id", "role"),
    )

class RoleSchema(spec.BaseModel):
    role: str
    is_main: bool

    @classmethod
    def from_model(cls, role: PlayerTeamRole):
        return cls(role=role.role.name, is_main=role.is_main)

class PlayerRoleSchema(spec.BaseModel):
    player: "PlayerSchema"
    role: RoleSchema


from models.player_team import PlayerTeam
from models.player import PlayerSchema

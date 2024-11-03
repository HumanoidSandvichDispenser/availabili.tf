from datetime import date, datetime, timedelta
import enum
from typing import List
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import TIMESTAMP, BigInteger, Boolean, Enum, ForeignKey, ForeignKeyConstraint, Integer, Interval, MetaData, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy_utc import UtcDateTime

import spec

class Base(DeclarativeBase):
    pass

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(model_class=Base, metadata=metadata)
migrate = Migrate(render_as_batch=True)

class Player(db.Model):
    __tablename__ = "players"

    steam_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(63))

    teams: Mapped[List["PlayerTeam"]] = relationship(back_populates="player")
    auth_sessions: Mapped[List["AuthSession"]] = relationship(back_populates="player")

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

class PlayerSpec(spec.BaseModel):
    steam_id: str
    username: str
    #teams: list["PlayerTeamSpec"]

class Team(db.Model):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(63), unique=True)
    discord_webhook_url: Mapped[str] = mapped_column(String(255), nullable=True)

    players: Mapped[List["PlayerTeam"]] = relationship(back_populates="team")

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

class TeamSpec(spec.BaseModel):
    id: int
    team_name: str
    discord_webhook_url: str | None
    #players: list[PlayerTeamSpec] | None

class PlayerTeam(db.Model):
    __tablename__ = "players_teams"

    class TeamRole(enum.Enum):
        Player = 0
        CoachMentor = 1

    player_id: Mapped[int] = mapped_column(ForeignKey("players.steam_id"), primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), primary_key=True)

    player: Mapped["Player"] = relationship(back_populates="teams")
    team: Mapped["Team"] = relationship(back_populates="players")

    player_roles: Mapped[List["PlayerTeamRole"]] = relationship(back_populates="player_team")
    availability: Mapped[List["PlayerTeamAvailability"]] = relationship(back_populates="player_team")

    team_role: Mapped[TeamRole] = mapped_column(Enum(TeamRole), default=TeamRole.Player)
    playtime: Mapped[timedelta] = mapped_column(Interval)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

class PlayerTeamRole(db.Model):
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

    role: Mapped[Role] = mapped_column(Enum(Role))
    is_main: Mapped[bool] = mapped_column(Boolean)

    __table_args__ = (
        ForeignKeyConstraint(
            [player_id, team_id],
            [PlayerTeam.player_id, PlayerTeam.team_id]
        ),
    )

class PlayerTeamAvailability(db.Model):
    __tablename__ = "players_teams_availability"

    player_id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[datetime] = mapped_column(UtcDateTime, primary_key=True)

    player_team: Mapped["PlayerTeam"] = relationship(
            "PlayerTeam",back_populates="availability")

    availability: Mapped[int] = mapped_column(Integer, default=2)
    end_time: Mapped[datetime] = mapped_column(UtcDateTime)

    __table_args__ = (
        ForeignKeyConstraint(
            [player_id, team_id],
            [PlayerTeam.player_id, PlayerTeam.team_id]
        ),
    )

class AuthSession(db.Model):
    __tablename__ = "auth_sessions"

    @staticmethod
    def gen_cookie_expiration():
        valid_until = date.today() + timedelta(days=7)
        AuthSession.gen_cookie_expiration()
        return valid_until

    key: Mapped[str] = mapped_column(String(31), primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.steam_id"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    player: Mapped["Player"] = relationship(back_populates="auth_sessions")

def init_db(app: Flask):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    db.init_app(app)
    migrate.init_app(app, db)
    return app

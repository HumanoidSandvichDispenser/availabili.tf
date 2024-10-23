# pyright: basic
import enum
import os
from sys import stderr
from typing import override
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, create_engine, Column, BigInteger, String, func
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

db_uri = os.getenv("DB_URI")

if db_uri is not str:
    db_uri = "sqlite:///./sqlite3/db.sqlite3"

engine = create_engine(db_uri)
Session = sessionmaker(bind=engine)

Base = declarative_base()
Base.metadata.create_all(engine)

class Player(Base):
    __tablename__ = "players"

    steam_id = Column(BigInteger, primary_key=True)
    name = Column(String)

    @override
    def __repr__(self):
        return str(self.name)

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String(63), nullable=False)

    @override
    def __repr__(self) -> str:
        return str(self.team_name)

class PlayerInfo(Base):
    __tablename__ = "playerinfo"

    player_id = Column(BigInteger, ForeignKey("players.steam_id"), primary_key=True)
    player = relationship("Player", back_populates="playerinfo")
    teams = relationship("Team", secondary="playerinfo_teams", back_populates="players")

class TeamRole(enum.Enum):
    PLAYER = "PL"
    COACH_MENTOR = "CM"
    TEAM_CAPTAIN = "TC"

class PlayerInfo_Team(Base):
    __tablename__ = "playerinfo_teams"

    playerinfo_id = Column(BigInteger, ForeignKey("playerinfo.player_id"), primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), primary_key=True)
    team_role = Column(Enum(TeamRole), default=TeamRole.PLAYER, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

class ClassRole(enum.Enum):
    P_SCOUT = "P_SCOUT"
    F_SCOUT = "F_SCOUT"
    SCOUT = "SCOUT"
    P_SOLLY = "P_SOLLY"
    ROAMER = "ROAMER"
    SOLDIER = "SOLDIER"
    PYRO = "PYRO"
    DEMO = "DEMO"
    HEAVY = "HEAVY"
    ENGIE = "ENGIE"
    MEDIC = "MEDIC"
    SNIPER = "SNIPER"
    SPY = "SPY"

class PlayerRole(Base):
    __tablename__ = "playerroles"

    playerinfo_id = Column(BigInteger, ForeignKey("playerinfo_teams.playerinfo_id"), primary_key=True)
    team_id = Column(Integer, ForeignKey("playerinfo_teams.team_id"), primary_key=True)
    class_role = Column(Enum(ClassRole), nullable=False, primary_key=True)
    main = Column(Boolean, default=True)

    @override
    def __repr__(self):
        return f"<PlayerRole(player_role={self.player_role}, main={self.main})>"

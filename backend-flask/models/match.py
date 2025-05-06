from datetime import datetime, timedelta
from typing import TypedDict
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP, Integer, Interval, String
import app_db
import spec


class Match(app_db.BaseModel):
    __tablename__ = "matches"

    logs_tf_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    logs_tf_title: Mapped[str] = mapped_column(String(255))
    duration: Mapped[int] = mapped_column(Integer)
    match_time: Mapped[datetime] = mapped_column(TIMESTAMP)
    blue_score: Mapped[int] = mapped_column(Integer)
    red_score: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    teams: Mapped[list["TeamMatch"]] = relationship("TeamMatch", back_populates="match")
    players: Mapped[list["PlayerMatch"]] = relationship("PlayerMatch", back_populates="match")

class MatchSchema(spec.BaseModel):
    logs_tf_id: int
    logs_tf_title: str
    duration: int
    match_time: datetime
    blue_score: int
    red_score: int
    created_at: datetime

    @classmethod
    def from_model(cls, model: Match):
        return cls(
            logs_tf_id=model.logs_tf_id,
            logs_tf_title=model.logs_tf_title,
            duration=model.duration,
            match_time=model.match_time,
            blue_score=model.blue_score,
            red_score=model.red_score,
            created_at=model.created_at
        )

class RawLogSummary:
    id: int
    title: str
    map: str
    date: int
    players: int
    views: int

    @classmethod
    def from_response(cls, response: dict):
        object = cls()
        object.id = response["id"]
        object.title = response["title"]
        object.map = response["map"]
        object.date = response["date"]
        object.players = response["players"]
        object.views = response["views"]
        return object

class LogTeam(TypedDict):
    score: int
    #kills: int
    #deaths: int
    #dmg: int
    #charges: int
    #drops: int
    #firstcaps: int
    #caps: int

class LogPlayer(TypedDict):
    team: str
    kills: int
    deaths: int
    assists: int
    dmg: int
    dt: int

class LogInfo(TypedDict):
    title: str
    map: str
    date: int

class LogRound(TypedDict):
    length: int

class RawLogDetails(TypedDict):
    teams: dict[str, LogTeam]
    players: dict[str, LogPlayer]
    #rounds: list[LogRound]
    info: LogInfo
    length: int


from models.team_match import TeamMatch
from models.player_match import PlayerMatch

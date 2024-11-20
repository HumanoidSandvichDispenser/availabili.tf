from datetime import UTC, datetime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP, Integer, SmallInteger, String
import app_db
import spec


class Team(app_db.BaseModel):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(63), unique=True)
    discord_webhook_url: Mapped[str] = mapped_column(String(255), nullable=True)
    tz_timezone: Mapped[str] = mapped_column(String(31), default="Etc/UTC")
    minute_offset: Mapped[int] = mapped_column(SmallInteger, default=0)

    players: Mapped[list["PlayerTeam"]] = relationship(back_populates="team")
    invites: Mapped[list["TeamInvite"]] = relationship(back_populates="team")
    integrations: Mapped[list["TeamIntegration"]] = relationship(back_populates="team")
    events: Mapped[list["Event"]] = relationship(back_populates="team")

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

class TeamSchema(spec.BaseModel):
    id: int
    team_name: str
    tz_timezone: str
    minute_offset: int
    created_at: datetime

    @classmethod
    def from_model(cls, team: Team):
        return cls(
            id=team.id,
            team_name=team.team_name,
            tz_timezone=team.tz_timezone,
            minute_offset=team.minute_offset,
            created_at=team.created_at,
        )

from models.player_team import PlayerTeam
from models.team_integration import TeamIntegration
from models.team_invite import TeamInvite
from models.event import Event

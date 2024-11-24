from datetime import datetime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.types import TIMESTAMP, Integer, String, Text
from sqlalchemy.sql import func
from sqlalchemy_utc import UtcDateTime
import app_db
import spec


class Event(app_db.BaseModel):
    __tablename__ = "events"

    # surrogate key
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    # primary key
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    start_time: Mapped[datetime] = mapped_column(UtcDateTime, nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    team: Mapped["Team"] = relationship("Team", back_populates="events")
    players: Mapped["PlayerEvent"] = relationship("PlayerEvent", back_populates="event")

    __table_args__ = (
        UniqueConstraint("team_id", "name", "start_time"),
    )

class EventSchema(spec.BaseModel):
    id: int
    team_id: int
    name: str
    description: str | None
    start_time: datetime
    created_at: datetime

    @classmethod
    def from_model(cls, model: Event) -> "EventSchema":
        return cls(
            id=model.id,
            name=model.name,
            description=model.description,
            start_time=model.start_time,
            team_id=model.team_id,
            created_at=model.created_at,
        )


from models.team import Team
from models.player_event import PlayerEvent

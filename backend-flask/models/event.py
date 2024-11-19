from datetime import datetime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.types import TIMESTAMP, Integer, String, Text
from sqlalchemy.sql import func
from sqlalchemy_utc import UtcDateTime
import app_db


class Event(app_db.BaseModel):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    start_time: Mapped[datetime] = mapped_column(UtcDateTime, nullable=False)
    team_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    team: Mapped["Team"] = relationship("Team", back_populates="events")


from models.team import Team

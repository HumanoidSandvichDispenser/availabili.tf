from datetime import datetime

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP, Boolean, String
import app_db
import spec


class TeamInvite(app_db.BaseModel):
    __tablename__ = "team_invites"

    key: Mapped[str] = mapped_column(String(31), primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    delete_on_use: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    team: Mapped["Team"] = relationship(back_populates="invites")

class TeamInviteSchema(spec.BaseModel):
    key: str
    team_id: int
    created_at: datetime


from models.team import Team

from datetime import date, datetime, timedelta

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP, String
import app_db


class AuthSession(app_db.BaseModel):
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


from models.player import Player

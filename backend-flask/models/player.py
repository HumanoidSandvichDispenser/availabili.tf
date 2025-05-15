from datetime import datetime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP, BigInteger, String
import app_db
import spec


class Player(app_db.BaseModel):
    __tablename__ = "players"

    steam_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(63))
    is_admin: Mapped[bool] = mapped_column(default=False)
    discord_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, unique=True)

    teams: Mapped[list["PlayerTeam"]] = relationship(back_populates="player")
    auth_sessions: Mapped[list["AuthSession"]] = relationship(back_populates="player")
    events: Mapped[list["PlayerEvent"]] = relationship(back_populates="player")
    matches: Mapped[list["PlayerMatch"]] = relationship(back_populates="player")

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

class PlayerSchema(spec.BaseModel):
    steam_id: str
    username: str
    is_admin: bool = False
    discord_id: str | None = None

    @classmethod
    def from_model(cls, player: Player):
        return cls(
            steam_id=str(player.steam_id),
            username=player.username,
            is_admin=player.is_admin,
            discord_id=str(player.discord_id) if player.discord_id else None
        )


from models.auth_session import AuthSession
from models.player_event import PlayerEvent
from models.player_team import PlayerTeam
from models.player_match import PlayerMatch

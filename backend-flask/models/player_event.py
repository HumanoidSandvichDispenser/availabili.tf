from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.orm.properties import ForeignKey
import app_db


class PlayerEvent(app_db.BaseModel):
    __tablename__ = "players_events"

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.steam_id"), primary_key=True)

    event: Mapped["Event"] = relationship("Event", back_populates="players")
    player: Mapped["Player"] = relationship("Player", back_populates="events")


from models.event import Event
from models.player import Player

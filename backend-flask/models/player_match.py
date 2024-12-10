from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import BigInteger, Integer
import app_db


class PlayerMatch(app_db.BaseModel):
    __tablename__ = "players_matches"

    player_id: Mapped[int] = mapped_column(ForeignKey("players.steam_id"), primary_key=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.logs_tf_id"), primary_key=True)

    kills: Mapped[int] = mapped_column(Integer)
    deaths: Mapped[int] = mapped_column(Integer)
    assists: Mapped[int] = mapped_column(Integer)
    damage: Mapped[int] = mapped_column(BigInteger)
    damage_taken: Mapped[int] = mapped_column(BigInteger)

    player: Mapped["Player"] = relationship("Player", back_populates="matches")
    match: Mapped["Match"] = relationship("Match", back_populates="players")


from models.match import Match
from models.player import Player

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.types import Integer
from sqlalchemy_utc import UtcDateTime
import app_db


class PlayerTeamAvailability(app_db.BaseModel):
    __tablename__ = "players_teams_availability"

    player_id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[datetime] = mapped_column(UtcDateTime, primary_key=True)

    player_team: Mapped["PlayerTeam"] = relationship(
            "PlayerTeam", back_populates="availability")

    availability: Mapped[int] = mapped_column(Integer, default=2)
    end_time: Mapped[datetime] = mapped_column(UtcDateTime)


    from models.player_team import PlayerTeam

    __table_args__ = (
        ForeignKeyConstraint(
            [player_id, team_id],
            [PlayerTeam.player_id, PlayerTeam.team_id]
        ),
    )

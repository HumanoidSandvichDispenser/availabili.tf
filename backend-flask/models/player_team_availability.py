from datetime import datetime, timedelta

from sqlalchemy.orm.properties import ForeignKey

import spec
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKeyConstraint
from sqlalchemy.types import BigInteger, Integer
from sqlalchemy_utc import UtcDateTime
import app_db


class PlayerTeamAvailability(app_db.BaseModel):
    __tablename__ = "players_teams_availability"

    player_team_id = mapped_column(ForeignKey("players_teams.id"), primary_key=True)
    start_time: Mapped[datetime] = mapped_column(UtcDateTime, primary_key=True, index=True)

    player_team: Mapped["PlayerTeam"] = relationship(
        "PlayerTeam",
        back_populates="availability",
    )

    availability: Mapped[int] = mapped_column(Integer, default=2)
    end_time: Mapped[datetime] = mapped_column(UtcDateTime, index=True)

class AvailabilitySchema(spec.BaseModel):
    steam_id: str
    username: str
    availability: list[int] = [0] * 168

    def add_availability_region(
        self,
        region: PlayerTeamAvailability,
        window_start: datetime,
    ):
        relative_start_time = region.start_time - window_start
        relative_start_hour = int(relative_start_time.total_seconds() // 3600)
        relative_end_time = region.end_time - window_start
        relative_end_hour = int(relative_end_time.total_seconds() // 3600)
        window_size_hours = 168  # TODO: change me if window_size is variable

        i = max(0, relative_start_hour)
        while i < window_size_hours and i < relative_end_hour:
            #print(i, "=", region.availability)
            self.availability[i] = region.availability
            i += 1

class PlayerTeamAvailabilityRoleSchema(spec.BaseModel):
    player: "PlayerSchema"
    playtime: int
    availability: int
    roles: list["RoleSchema"]


from models.player import PlayerSchema
from models.player_team_role import RoleSchema
from models.player_team import PlayerTeam

from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.types import Integer, String
import app_db


class TeamIntegration(app_db.BaseModel):
    __tablename__ = "team_integrations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("teams.id"))
    integration_type: Mapped[str]

    team: Mapped["Team"] = relationship(back_populates="integrations")

    __mapper_args__ = {
        "polymorphic_identity": "team_integrations",
        "polymorphic_on": "integration_type",
    }

class TeamDiscordIntegration(TeamIntegration):
    __tablename__ = "team_discord_integrations"

    integration_id: Mapped[int] = mapped_column(ForeignKey("team_integrations.id"), primary_key=True)
    webhook_url: Mapped[str] = mapped_column(String(255))

    __mapper_args__ = {
        "polymorphic_identity": "team_discord_integrations",
    }

from models.team import Team

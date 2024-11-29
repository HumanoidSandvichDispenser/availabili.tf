from typing import Optional
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.types import Integer, String
import app_db
import spec


class TeamDiscordIntegration(app_db.BaseModel):
    __tablename__ = "team_discord_integrations"

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), primary_key=True)
    webhook_url: Mapped[str] = mapped_column(String)
    webhook_bot_name: Mapped[str] = mapped_column(String)
    webhook_bot_profile_picture: Mapped[str] = mapped_column(String(255), nullable=True)

    team: Mapped["Team"] = relationship("Team", back_populates="discord_integration")

class TeamDiscordIntegrationSchema(spec.BaseModel):
    webhook_url: str
    webhook_bot_name: str
    webhook_bot_profile_picture: Optional[str]

    @classmethod
    def from_model(cls, model: TeamDiscordIntegration) -> "TeamDiscordIntegrationSchema":
        return cls(
            webhook_url=model.webhook_url,
            webhook_bot_name=model.webhook_bot_name,
            webhook_bot_profile_picture=model.webhook_bot_profile_picture,
        )

class TeamLogsTfIntegration(app_db.BaseModel):
    __tablename__ = "team_logs_tf_integrations"

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), primary_key=True)
    logs_tf_api_key: Mapped[str | None] = mapped_column(String, nullable=True)

    # requires at least this many team members in a single team in the log to
    # be automatically loaded into the database
    min_team_member_count: Mapped[int] = mapped_column(Integer, default=4)

    team: Mapped["Team"] = relationship("Team", back_populates="logs_tf_integration")

class TeamLogsTfIntegrationSchema(spec.BaseModel):
    logs_tf_api_key: str | None
    min_team_member_count: int

    @classmethod
    def from_model(cls, model: TeamLogsTfIntegration) -> "TeamLogsTfIntegrationSchema":
        return cls(
            logs_tf_api_key=model.logs_tf_api_key,
            min_team_member_count=model.min_team_member_count,
        )

class TeamIntegrationSchema(spec.BaseModel):
    discord_integration: TeamDiscordIntegrationSchema | None
    logs_tf_integration: TeamLogsTfIntegrationSchema | None


from models.team import Team

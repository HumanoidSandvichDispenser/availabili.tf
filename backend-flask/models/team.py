from datetime import UTC, datetime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP, Integer, SmallInteger, String
import app_db
import spec


class Team(app_db.BaseModel):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(63), unique=True)
    discord_webhook_url: Mapped[str] = mapped_column(String(255), nullable=True)
    tz_timezone: Mapped[str] = mapped_column(String(31), default="Etc/UTC")
    minute_offset: Mapped[int] = mapped_column(SmallInteger, default=0)

    players: Mapped[list["PlayerTeam"]] = relationship(back_populates="team")
    invites: Mapped[list["TeamInvite"]] = relationship(back_populates="team")
    events: Mapped[list["Event"]] = relationship(back_populates="team")

    discord_integration: Mapped["TeamDiscordIntegration"] = relationship(
        "TeamDiscordIntegration",
        back_populates="team",
        uselist=False,
        lazy="raise",
    )

    logs_tf_integration: Mapped["TeamLogsTfIntegration"] = relationship(
        "TeamLogsTfIntegration",
        back_populates="team",
        uselist=False,
        lazy="raise",
    )

    matches: Mapped[list["TeamMatch"]] = relationship(back_populates="team")

    def update_integrations(self, integrations: "TeamIntegrationSchema"):
        if integrations.discord_integration:
            discord_integration = self.discord_integration \
                or TeamDiscordIntegration()
            discord_integration.webhook_url = integrations \
                .discord_integration.webhook_url
            discord_integration.webhook_bot_name = integrations \
                .discord_integration.webhook_bot_name

            if integrations.discord_integration.webhook_bot_profile_picture:
                discord_integration.webhook_bot_profile_picture = integrations \
                    .discord_integration.webhook_bot_profile_picture

            if discord_integration.team_id is None:
                discord_integration.team_id = self.id
                app_db.db.session.add(discord_integration)
        elif self.discord_integration:
            app_db.db.session.delete(self.discord_integration)

        if integrations.logs_tf_integration:
            logs_tf_integration = self.logs_tf_integration \
                or TeamLogsTfIntegration()
            logs_tf_integration.logs_tf_api_key = integrations \
                .logs_tf_integration.logs_tf_api_key or ""
            logs_tf_integration.min_team_member_count = integrations \
                .logs_tf_integration.min_team_member_count

            if logs_tf_integration.team_id is None:
                logs_tf_integration.team_id = self.id
                app_db.db.session.add(logs_tf_integration)
        elif self.logs_tf_integration:
            app_db.db.session.delete(self.logs_tf_integration)

    def get_integrations(self) -> "TeamIntegrationSchema":
        discord_integration = None
        logs_tf_integration = None
        if self.discord_integration:
            discord_integration = TeamDiscordIntegrationSchema.from_model(
                self.discord_integration
            )
        if self.logs_tf_integration:
            logs_tf_integration = TeamLogsTfIntegrationSchema.from_model(
                self.logs_tf_integration
            )
        return TeamIntegrationSchema(
            discord_integration=discord_integration,
            logs_tf_integration=logs_tf_integration,
        )

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

class TeamSchema(spec.BaseModel):
    id: int
    team_name: str
    tz_timezone: str
    minute_offset: int
    created_at: datetime

    @classmethod
    def from_model(cls, team: Team):
        return cls(
            id=team.id,
            team_name=team.team_name,
            tz_timezone=team.tz_timezone,
            minute_offset=team.minute_offset,
            created_at=team.created_at,
        )

class TeamWithRoleSchema(TeamSchema):
    role: str
    is_team_leader: bool
    player_count: int

    @classmethod
    def from_player_team(cls, player_team: "PlayerTeam"):
        return cls(
            id=player_team.team.id,
            team_name=player_team.team.team_name,
            tz_timezone=player_team.team.tz_timezone,
            minute_offset=player_team.team.minute_offset,
            created_at=player_team.team.created_at,
            role=player_team.team_role.name,
            is_team_leader=player_team.is_team_leader,
            player_count=len(player_team.team.players),
        )

from models.player_team import PlayerTeam
from models.team_invite import TeamInvite
from models.team_integration import (
    TeamDiscordIntegration,
    TeamDiscordIntegrationSchema,
    TeamIntegrationSchema,
    TeamLogsTfIntegration,
    TeamLogsTfIntegrationSchema,
)
from models.event import Event
from models.team_match import TeamMatch

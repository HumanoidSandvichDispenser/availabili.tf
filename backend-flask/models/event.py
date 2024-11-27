from datetime import datetime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.types import TIMESTAMP, BigInteger, Integer, String, Text
from sqlalchemy.sql import func
from sqlalchemy_utc import UtcDateTime
from discord_webhook import DiscordWebhook
import app_db
import spec


class Event(app_db.BaseModel):
    __tablename__ = "events"

    # surrogate key
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    # primary key
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    start_time: Mapped[datetime] = mapped_column(UtcDateTime, nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    discord_message_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    team: Mapped["Team"] = relationship("Team", back_populates="events")
    players: Mapped[list["PlayerEvent"]] = relationship("PlayerEvent", back_populates="event")

    __table_args__ = (
        UniqueConstraint("team_id", "name", "start_time"),
    )

    def get_discord_content(self):
        start_timestamp = int(self.start_time.timestamp())
        players = list(self.players)
        # players with a role should be sorted first
        players.sort(key=lambda p: p.role is not None, reverse=True)
        players_info = []

        for player in players:
            player_info = "- "

            if player.role:
                player_info += f"**{player.role.role.name}:** "

            player_info += f"{player.player.username}"

            if player.has_confirmed:
                player_info += " ✅"
            else:
                player_info += " ⏳"

            players_info.append(player_info)

        return "\n".join([
            f"# {self.name}",
            "",
            self.description or "*No description.*",
            "",
            f"<t:{start_timestamp}:f>",
            "\n".join(players_info),
            "",
            "[Confirm availability here]" +
                f"(https://availabili.tf/team/id/{self.team.id}/events/{self.id})",
        ])

    def get_or_create_webhook(self):
        integration = app_db.db.session.query(
            TeamDiscordIntegration
        ).where(
            TeamDiscordIntegration.team_id == self.team_id
        ).first()

        if not integration:
            return None

        if self.discord_message_id:
            return DiscordWebhook(
                integration.webhook_url,
                id=str(self.discord_message_id),
            )
        else:
            return DiscordWebhook(integration.webhook_url)

    def update_discord_message(self):
        webhook = self.get_or_create_webhook()
        if webhook:
            webhook.content = self.get_discord_content()
            if webhook.id:
                webhook.edit()
            else:
                webhook.execute()
                if webhook_id := webhook.id:
                    self.discord_message_id = int(webhook_id)
                    app_db.db.session.commit()
                else:
                    raise Exception("Failed to create webhook")

class EventSchema(spec.BaseModel):
    id: int
    team_id: int
    name: str
    description: str | None
    start_time: datetime
    created_at: datetime

    @classmethod
    def from_model(cls, model: Event) -> "EventSchema":
        return cls(
            id=model.id,
            name=model.name,
            description=model.description,
            start_time=model.start_time,
            team_id=model.team_id,
            created_at=model.created_at,
        )

class EventPlayersSchema(spec.BaseModel):
    players: list["PlayerEventRolesSchema"]

    @classmethod
    def from_model(cls, model: Event) -> "EventPlayersSchema":
        return cls(
            players=[PlayerEventRolesSchema.from_model(player) for player in model.players],
            roles=[RoleSchema.from_model(player.role.role) for player in model.players if player.role],
        )


from models.team import Team
from models.player_event import PlayerEvent
from models.team_integration import TeamDiscordIntegration

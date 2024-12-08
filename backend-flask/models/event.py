from datetime import datetime
import threading
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

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    discord_message_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    team: Mapped["Team"] = relationship("Team", back_populates="events")
    players: Mapped[list["PlayerEvent"]] = relationship(
        "PlayerEvent",
        back_populates="event",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("team_id", "name", "start_time"),
    )

    def get_maximum_matching(self):
        players_teams_roles = app_db.db.session.query(
            PlayerTeamRole
        ).join(
            PlayerTeam
        ).join(
            PlayerEvent,
            PlayerTeam.player_id == PlayerEvent.player_id
        ).where(
            PlayerTeam.team_id == self.team_id
        ).where(
            PlayerTeam.player_id == PlayerEvent.player_id
        ).where(
            PlayerEvent.event_id == self.id
        ).all()

        role_map = {}
        for roles in players_teams_roles:
            if roles.player_team_id not in role_map:
                role_map[roles.player_team_id] = []
            role_map[roles.player_team_id].append(roles.role)
        import sys
        print(role_map, file=sys.stderr)

        required_roles = [
            PlayerTeamRole.Role.PocketScout,
            PlayerTeamRole.Role.FlankScout,
            PlayerTeamRole.Role.PocketSoldier,
            PlayerTeamRole.Role.Roamer,
            PlayerTeamRole.Role.Demoman,
            PlayerTeamRole.Role.Medic,
        ]
        graph = BipartiteGraph(role_map, required_roles)
        return graph.hopcroft_karp()

    def get_discord_content(self):
        start_timestamp = int(self.start_time.timestamp())
        players = list(self.players)
        # players with a role should be sorted first
        players.sort(key=lambda p: p.role is not None, reverse=True)
        players_info = []
        matchings = self.get_maximum_matching()
        ringers_needed = 6 - matchings

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

        ringers_needed_msg = ""
        if ringers_needed > 0:
            ringers_needed_msg = f" **({ringers_needed} ringer(s) needed)**"

        return "\n".join([
            f"# {self.name}",
            "",
            self.description or "*No description.*",
            "",
            f"<t:{start_timestamp}:f>",
            "\n".join(players_info),
            f"Max bipartite matching size: {matchings}" + ringers_needed_msg,
            "",
            "[Confirm attendance here]" +
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
                username=integration.webhook_bot_name,
                avatar_url=integration.webhook_bot_profile_picture,
            )
        else:
            return DiscordWebhook(
                integration.webhook_url,
                username=integration.webhook_bot_name,
                avatar_url=integration.webhook_bot_profile_picture,
            )

    def update_discord_message(self):
        webhook = self.get_or_create_webhook()
        if webhook:
            webhook.content = self.get_discord_content()
            if webhook.id:
                # fire and forget
                threading.Thread(target=webhook.edit).start()
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

#class EventPlayersSchema(spec.BaseModel):
#    players: list["PlayerEventRolesSchema"]
#
#    @classmethod
#    def from_model(cls, model: Event) -> "EventPlayersSchema":
#        return cls(
#            players=[PlayerEventRolesSchema.from_model(player) for player in model.players],
#            roles=[RoleSchema.from_model(player.role.role) for player in model.players if player.role],
#        )


from models.team import Team
from models.player_event import PlayerEvent, PlayerEventRolesSchema
from models.team_integration import TeamDiscordIntegration
from models.player_team import PlayerTeam
from models.player_team_role import PlayerTeamRole
from utils.bipartite_graph import BipartiteGraph

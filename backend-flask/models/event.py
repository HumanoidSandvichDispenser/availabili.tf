from datetime import datetime
import requests
import threading
from models.player import Player
from sqlalchemy.orm import mapped_column, relationship, scoped_session
from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.orm.properties import ForeignKey
from sqlalchemy.orm.session import Session
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.types import TIMESTAMP, BigInteger, Integer, String, Text
from sqlalchemy.sql import func
from sqlalchemy_utc import UtcDateTime
import app_db
import spec
import os


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
    discord_message_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, unique=True)

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
        players_teams_roles = app_db.db_session.query(
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

        # TODO: write this to use a single query
        players: list[PlayerEvent] = list(self.players)
        non_players = app_db.db_session.query(
            PlayerTeam
        ).where(
            PlayerTeam.team_id == self.team_id,
            PlayerTeam.player_id.not_in([p.player_id for p in players])
        ).all()

        # players should be sorted by their role, leaving no-role players last
        players.sort(key=lambda p: p.role.role.value if p.role else 1023)
        players_info = []
        non_players_info = ""
        matchings = self.get_maximum_matching()
        ringers_needed = 6 - matchings

        role_emojis = {
            "blank": "1373226295651209226",
            "Spy": "1373040448561741895",
            "Sniper": "1373040439250255932",
            "Medic": "1373040382492938385",
            "Engineer": "1373040371415781467",
            "Heavy": "1373040363060592720",
            "Demoman": "1373040354470924400",
            "Pyro": "1373040345197187145",
            "Roamer": "1373040339144806420",
            "PocketSoldier": "1373040333775962132",
            "Soldier": "1373040326872141924",
            "FlankScout": "1373040315187073034",
            "Scout": "1373040306089623663",
            "PocketScout": "1373040277924614254"
        }

        for player in players:
            player_info = ""

            if player.role:
                player_info += "<:" + player.role.role.name + ":" + role_emojis.get(
                    player.role.role.name, "1373226295651209226"
                ) + ">"
            else:
                player_info += "<:blank:1373226295651209226>"

            if player.has_confirmed:
                player_info += " ✅"
            else:
                player_info += " ⏳"

            if player.player.discord_id:
                player_info += f" <@{player.player.discord_id}>"
            else:
                player_info += f" {player.player.username}"

            players_info.append(player_info)

        non_players_info = "<:blank:1373226295651209226> ❌ "
        non_players_info += ", ".join(
            [
                f"<@{player.player.discord_id}>"
                if player.player.discord_id
                else player.player.username
                for player in non_players
            ]
        )

        ringers_needed_msg = ""
        if ringers_needed > 0:
            if ringers_needed == 1:
                ringers_needed_msg = " **(1 ringer needed)**"
            else:
                ringers_needed_msg = f" **({ringers_needed} ringers needed)**"

        return "\n".join([
            f"# {self.name}",
            "",
            self.description or "*No description.*",
            "",
            f"<t:{start_timestamp}:f>",
            "\n".join(players_info),
            non_players_info,
            f"Maximum roles filled: {matchings}" + ringers_needed_msg,
            #"",
            #"[Confirm attendance here]" +
            #    f"(https://{domain}/team/id/{self.team.id})",
        ])

    def get_discord_message_components(self):
        domain = os.environ.get("DOMAIN", "availabili.tf")

        return [
            {
                "type": 10,
                "content": self.get_discord_content(),
            },
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "label": "✅",
                        "style": 3,
                        "custom_id": "click_attending"
                    },
                    {
                        "type": 2,
                        "label": "⌛",
                        "style": 2,
                        "custom_id": "click_pending"
                    },
                    {
                        "type": 2,
                        "label": "❌",
                        "style": 2,
                        "custom_id": "click_not_attending"
                    },
                    {
                        "type": 2,
                        "label": "Edit",
                        "style": 2,
                        "custom_id": "click_edit_event"
                    },
                    {
                        "type": 2,
                        "label": "View in browser",
                        "style": 5,
                        "url": f"https://{domain}/team/id/{self.team_id}"
                    }
                ]
            }
        ]

    def get_or_create_webhook(self):
        integration = app_db.db_session.query(
            TeamDiscordIntegration
        ).where(
            TeamDiscordIntegration.team_id == self.team_id
        ).first()

        if not integration:
            return None, ""

        webhook = {
            "username": integration.webhook_bot_name,
            "avatar_url": integration.webhook_bot_profile_picture,
            "flags": 1 << 15,
        }

        return webhook, integration.webhook_url

    def update_discord_message(self):
        domain = os.environ.get("DOMAIN", "availabili.tf")
        webhook, webhook_url = self.get_or_create_webhook()
        if webhook:
            params = "?with_components=true&wait=true"
            webhook["components"] = self.get_discord_message_components()
            if self.discord_message_id:
                # fire and forget
                #threading.Thread(target=webhook.edit).start()
                del webhook["username"]
                del webhook["avatar_url"]
                webhook_url += f"/messages/{self.discord_message_id}"
                requests.patch(webhook_url + params, json=webhook)
            else:
                #webhook.execute()
                response = requests.post(webhook_url + params, json=webhook)
                response = response.json()

                if webhook_id := response["id"]:
                    self.discord_message_id = int(webhook_id)
                    app_db.db_session.commit()
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

import os
import discord
from discord.ext import commands
import app_db
import models
from models.event import Event
from models.player import Player
from models.player_event import PlayerEvent
from models.player_team import PlayerTeam

app_db.db_session = app_db.create_isolated_db_session(None)

guild_id_str = os.getenv("GUILD_ID")
guild_id = discord.Object(id=int(guild_id_str)) if guild_id_str else None

discord_token = os.getenv("DISCORD_TOKEN")

if not discord_token:
    raise ValueError("DISCORD_TOKEN environment variable not set.")

class EventModal(discord.ui.Modal):
    event_name = discord.ui.TextInput(
        label="Event Name",
        placeholder="Enter the event name",
    )

    event_description = discord.ui.TextInput(
        label="Event Description",
        placeholder="Describe the event",
        style=discord.TextStyle.long,
    )

    def __init__(self, event: Event):
        self.event = event
        self.event_name.default = event.name
        self.event_description.default = event.description
        super().__init__(title="Event Details")

    async def on_submit(self, interaction: discord.Interaction):
        player_team = app_db.db_session.query(
            PlayerTeam
        ).where(
            PlayerTeam.team_id == self.event.team_id,
        ).join(
            Player,
            Player.steam_id == PlayerTeam.player_id
        ).where(
            Player.discord_id == interaction.user.id
        ).one_or_none()

        if not player_team or not player_team.is_team_leader:
            await interaction.response.send_message(
                "You are not authorized to edit this event.",
                ephemeral=True
            )

        self.event.name = self.event_name.value
        self.event.description = self.event_description.value
        app_db.db_session.commit()
        self.event.update_discord_message()

        await interaction.response.send_message("Event details updated.", ephemeral=True)

async def handle_update_attendance(
    player: Player,
    event: Event,
    interaction: discord.Interaction,
    custom_id: str
):
    player_event = app_db.db_session.query(
        PlayerEvent
    ).where(
        PlayerEvent.player_id == player.steam_id,
        PlayerEvent.event_id == event.id
    ).one_or_none()

    if custom_id == "click_not_attending":
        if player_event:
            app_db.db_session.delete(player_event)
            app_db.db_session.commit()
            event.update_discord_message()
            await interaction.response.defer()
        return
    
    if not player_event:
        player_event = PlayerEvent()
        player_event.event_id = event.id
        player_event.player_id = player.steam_id
        app_db.db_session.add(player_event)

    player_event.has_confirmed = custom_id == "click_attending"
    app_db.db_session.commit()
    event.update_discord_message()
    await interaction.response.defer()

class Client(commands.Bot):
    async def on_ready(self):
        if guild_id:
            try:
                synced = await self.tree.sync(guild=guild_id)
                print(f"Ready! Synced {len(synced)} commands.")
            except Exception as e:
                print(f"Failed to sync commands: {e}")
        pass

    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.response.is_done():
            return

        if interaction.type == discord.InteractionType.component and interaction.message:
            # Handle button interactions here
            if interaction.data is None or not "custom_id" in interaction.data:
                return

            interactions = [
                "click_attending",
                "click_pending",
                "click_not_attending",
                "click_edit_event",
            ]

            if interaction.data["custom_id"] in interactions:
                interaction_type = interaction.data["custom_id"]

                player = app_db.db_session.query(
                    Player
                ).where(
                    Player.discord_id == interaction.user.id
                ).one_or_none()

                if not player:
                    await interaction.response.send_message(
                        "This Discord account is not linked to a player. " +
                        "Contact <@195789918474207233> to link your account.",
                        ephemeral=True
                    )

                    # log the interaction
                    user = await self.fetch_user(195789918474207233)
                    if user:
                        await user.send(
                            f"User <@{interaction.user.id}> tried to " +
                            "interact with an event but their account is " +
                            "not linked to a player."
                        )
                    return

                event = app_db.db_session.query(
                    Event
                ).where(
                    Event.discord_message_id == interaction.message.id
                ).one_or_none()

                if event and player:
                    if interaction_type == "click_edit_event":
                        await interaction.response.send_modal(EventModal(event))
                    else:
                        await handle_update_attendance(player, event, interaction, interaction_type)

intents = discord.Intents.default()
client = Client(command_prefix="!", intents=intents)

@client.tree.command(
    name="setup-announcement-webhook",
    description="Set up announcements webhook in this channel",
    guild=guild_id
)
@discord.app_commands.guild_only()
@discord.app_commands.default_permissions(manage_webhooks=True)
async def setup_announcements(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Setting up announcement webhook. Any existing webhooks madde by " +
        "this command will be deleted.",
        ephemeral=True
    )

    channel = interaction.channel

    assert isinstance(channel, discord.TextChannel)

    for webhook in await channel.webhooks():
        if webhook.user == client.user:
            await webhook.delete()

    webhook = await channel.create_webhook(name="availabili.tf webhook")
    content = (
        f"Webhook created: {webhook.url}\n" + 
        "Use this webhook URL in the Discord integration settings of your " +
        "team to receive interactive announcements."
    )
    await interaction.followup.send(content, ephemeral=True)

client.run(discord_token)

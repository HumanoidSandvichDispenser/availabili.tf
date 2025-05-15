import os
import discord
from discord.ext import commands
import app_db
import models
from models.event import Event
from models.player import Player
from models.player_event import PlayerEvent

app_db.db_session = app_db.create_isolated_db_session(None)

guild_id_str = os.getenv("GUILD_ID")
guild_id = discord.Object(id=int(guild_id_str)) if guild_id_str else None

discord_token = os.getenv("DISCORD_TOKEN")

if not discord_token:
    raise ValueError("DISCORD_TOKEN environment variable not set.")

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

            has_interaction = False

            if interaction.data["custom_id"] == "click_attending":
                has_interaction = True
            elif interaction.data["custom_id"] == "click_pending":
                has_interaction = True
            elif interaction.data["custom_id"] == "click_not_attending":
                has_interaction = True

            if has_interaction:
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
                    return

                event = app_db.db_session.query(
                    Event
                ).where(
                    Event.discord_message_id == interaction.message.id
                ).one_or_none()

                if event and player:
                    player_event = app_db.db_session.query(
                        PlayerEvent
                    ).where(
                        PlayerEvent.player_id == player.steam_id,
                        PlayerEvent.event_id == event.id
                    ).one_or_none()

                    if interaction_type == "click_not_attending":
                        if player_event:
                            app_db.db_session.delete(player_event)
                            app_db.db_session.commit()
                            event.update_discord_message()
                            await interaction.response.defer()

                    if not player_event:
                        player_event = PlayerEvent()
                        player_event.event_id = event.id
                        player_event.player_id = player.steam_id
                        app_db.db_session.add(player_event)

                    player_event.has_confirmed = interaction_type == "click_attending"
                    app_db.db_session.commit()
                    event.update_discord_message()
                    await interaction.response.defer()

intents = discord.Intents.default()
client = Client(command_prefix="!", intents=intents)

@client.tree.command(
    name="setup-announcement-webhook",
    description="Set up announcements webhook in this channel",
    guild=guild_id
)
@discord.app_commands.default_permissions(manage_webhooks=True)
async def setup_announcements(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Setting up announcement webhook. Any existing webhooks madde by " +
        "this command will be deleted.",
        ephemeral=True
    )

    channel = interaction.channel

    if not isinstance(channel, discord.TextChannel):
        await interaction.followup.send(
            "This command can only be used in a text channel.",
            ephemeral=True
        )
        return

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

#@client.tree.command(
#    name="link-team",
#    description="Link this Discord guild to a team with an invite key",
#    guild=guild_id
#)
#@app_commands.describe(key="Team invite key")
#async def link_team(interaction: discord.Interaction, key: str):
#    team_invite = db_session.query(
#        models.TeamInvite
#    ).where(
#        models.TeamInvite.key == key
#    ).one_or_none()
#
#    if not team_invite:
#        await interaction.response.send_message(
#            "Invalid team invite key.",
#            ephemeral=True
#        )
#        return
#
#    # consume the invite and link the team to the guild

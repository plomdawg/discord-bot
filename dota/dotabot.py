import logging
import os
import sys

import discord
from discord.commands.context import ApplicationContext

# hacky way to import plomcord
sys.path.append(".") # Adds higher directory to python modules path.
import plomcord

# Get secret tokens from environment variables.
DISCORD_CLIENT_ID = os.environ.get('DISCORD_CLIENT_ID')
DISCORD_SECRET_TOKEN = os.environ.get('DISCORD_SECRET_TOKEN')

# Make sure we got them.
if DISCORD_CLIENT_ID is None:
    print("ERROR: DISCORD_CLIENT_ID not set.")
    sys.exit(1)

if DISCORD_SECRET_TOKEN is None:
    print("ERROR: DISCORD_SECRET_TOKEN not set.")
    sys.exit(1)

# Set up discord module logging.
discord_logger = logging.getLogger('discord')

# Set up our logging.
if os.environ.get('VERBOSE_LOGGING') is not None:
    discord_logger.setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.DEBUG)
else:
    discord_logger.setLevel(logging.INFO)
    logging.getLogger().setLevel(logging.DEBUG)


class DotaBot(discord.Bot):
    def __init__(self):
        # Call the parent constructor with all intents enabled.
        super().__init__(intents=discord.Intents.all())
        
        # Permission integer is calculated from https://discordapi.com/permissions.html
        self.permissions = 545447734385

        # Expose Client ID and invite link to the cogs.
        self.client_id = DISCORD_CLIENT_ID
        self.invite_link = f"https://discord.com/api/oauth2/authorize?client_id={self.client_id}"
        self.invite_link += f"&permissions={self.permissions}&scope=bot%20applications.commands"

        # Load cogs.
        self.load_extension('cogs.audio')
        self.load_extension('cogs.error_handler')
        self.load_extension('dota.cogs.wiki')
        self.load_extension('dota.cogs.database')
        self.load_extension('dota.cogs.emojis')
        self.load_extension('dota.cogs.quiz')
        self.load_extension('dota.cogs.help')
        self.load_extension('dota.cogs.voice_lines')


        @self.event
        async def on_ready():
            """ Called after the bot successfully connects to Discord servers """
            # Print some info.
            plomcord.on_ready_info(self)
            
            # Set our custom activity.
            await plomcord.set_activity(self, f"Playing in {len(self.guilds)} guilds")

            # Load emojis now that we're connected to discord servers.
            self.get_cog('Emojis').load_emojis()

            # Load the quiz now that the emojis are loaded.
            self.get_cog('ShopkeeperQuiz').load_words()

        @self.event
        async def on_guild_join(guild):
            # Try to find the #general channel to send first message.
            channel = discord.utils.get(guild.text_channels, name="general")
            # Fall back to the first text channel if there's no #general.
            if len(guild.text_channels) > 0 and channel is None:
                channel = guild.text_channels[0]
            await channel.send('Hello! You can send either a full quote with exact punctuation ("Haha!") or a partial quote prefixed by "dota" ("dota haha")')
            await channel.send('Support server: https://discord.gg/Czj2g9c')
            
            
        @self.event
        async def on_voice_state_update(member, before, after):
            """ Called when a user changes their voice state. """
            await plomcord.auto_disconnect(self, member.guild, seconds_to_wait=30)

def main():
    # Create the bot.
    bot = DotaBot()
    # Print the invite link.
    print(f"Invite link: {bot.invite_link}")
    # Run the bot.
    bot.run(DISCORD_SECRET_TOKEN)


if __name__ == '__main__':
    main()

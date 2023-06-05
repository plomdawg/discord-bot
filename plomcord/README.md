# plomcord

plomcord is a utility library enhancing the functionality of Discord bots built with Pycord. It provides a set of helpful functions to achieve common tasks, such as sending embeds, handling bot presence, managing reactions, and more.

## Installation

Before using this library, make sure you have installed Pycord by following the instructions in [Pycord repository](https://github.com/Pycord-Development/pycord).

To use plomcord in your bot, simply copy `plomcord.py` to your bot's project folder and import it using:
```python
import plomcord
```

## Available Functions

Here is a list of functions provided by plomcord:

- `on_ready_info(bot)`: Prints information about the bot when it connects to Discord servers.
- `auto_disconnect(bot, guild, seconds_to_wait=60)`: Leaves and clears the queue if the bot is left alone.
- `add_reactions(message, emojis)`: Adds emojis to a message, ignoring NotFound errors.
- `delete_message(message)`: Deletes a message, ignoring NotFound errors.
- `set_activity(bot, activity: str)`: Sets the bot's activity based on a string.
- `send_embed(channel, color=None, footer=None, footer_icon=None, subtitle=None, subtext=None, text=None, title=None, thumbnail=None)`: Sends a message to a channel, and returns the sent message.


# Example Usage

Here's a simple MVP bot using the plomcord utility functions with the Pycord library.

```python
import discord
from discord.ext import commands
import plomcord

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    plomcord.on_ready_info(bot)
    activity = "Listening to !help"
    await plomcord.set_activity(bot, activity)

@bot.command()
async def delete(ctx, message_id: int):
    message = await ctx.channel.fetch_message(message_id)
    await plomcord.delete_message(message)

@bot.command()
async def react(ctx, message_id: int, *emojis: discord.Emoji):
    message = await ctx.channel.fetch_message(message_id)
    await plomcord.add_reactions(message, emojis)

@bot.command()
async def embed(ctx, *text):
    content = ' '.join(text)
    await plomcord.send_embed(
        ctx,
        color=0xFF5733,
        title="Test Embed",
        text="This is the body of the embed.",
        subtitle="Subtitle",
        subtext="This is the subtext."
    )

@bot.command()
async def set_status(ctx, *, status):
    await plomcord.set_activity(ctx.bot, status)

bot.run("Your-Token-Here")
```

Replace the `"Your-Token-Here"` with your bot's secret token.

The embed command will send an embed like this:

![image](https://github.com/plomdawg/discord-bot/assets/6510862/0bf3d6dc-786d-418a-87dc-f9d8ece693e8)

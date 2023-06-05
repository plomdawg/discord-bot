# Utility functions used by various bots.
import discord
import random
import logging
import asyncio

def on_ready_info(bot):
    """ Prints information about the bot when it connects to Discord servers. """
    logging.info(
        f"Connected to {len(bot.guilds)} servers as {bot.user.name} ({bot.user.id})")

    # Print the invite link.
    invite_url = f"https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions={bot.permissions}"
    logging.info(invite_url)

    # Print guild info
    print(f"Connected to {len(bot.guilds)} servers:")
    user_count = 0
    for guild in bot.guilds:
        try:
            count = len(guild.members) - 1  # remove self from list
            print(
                f" - [{guild.id}] ({count} users) {guild.name} (Owner: {guild.owner.name}#{guild.owner.discriminator} {guild.owner.id})")
            # add user count, exclude discord bot list
            if guild.id != 264445053596991498:
                user_count += count
        except AttributeError:
            pass
    print(f"Total user reach: {user_count}")

async def auto_disconnect(bot, guild, seconds_to_wait=60):
    """ Leaves and clears the queue if the bot is left alone. """
    # Try to find the voice client for this guild.
    voice_client = None
    for vc in bot.voice_clients:
        if vc.guild == guild:
            voice_client = vc
            break

    # Nothing to do if the bot is not in a voice channel.
    if voice_client is None:
        return

    # If there are any non-bots in the channel, do nothing.
    if any([not user.bot for user in voice_client.channel.members]):
        return

    # Save the bot's current channel.
    bot_channel = voice_client.channel

    # If the bot is alone in the channel, start the timer.
    # Loop until somebody comes back, or the timer runs out.
    times_to_check = 3
    step_seconds = seconds_to_wait / times_to_check
    for _ in range(0, times_to_check):
        await asyncio.sleep(step_seconds)

        # Check if a non-bot has joined the channel.
        if any([not user.bot for user in voice_client.channel.members]):
            return

        # Check if the bot has been disconnected.
        if voice_client is None or not voice_client.is_connected():
            return

        # Check if the bot has been moved to a different channel.
        if voice_client.channel is not bot_channel:
            return

    # If the bot is still alone, disconnect.
    audio_player = bot.audio.get_audio_player(guild.id)
    await audio_player.stop()

async def add_reactions(message, emojis):
    """ Adds emojis to a message, ignoring NotFound errors """
    logging.debug(f"add_reactions({message.id}, {emojis})")
    if message is not None:
        try:
            for emoji in emojis:
                await message.add_reaction(emoji)
                await asyncio.sleep(0.1)
        except discord.errors.NotFound:
            return

async def delete_message(message):
    """ Deletes a message, ignoring NotFound errors """
    logging.debug(f"delete_message({message.id})")
    if message is not None:
        try:
            logging.debug(f"type(message) = {type(message)}")
            await message.delete()
        except discord.errors.NotFound:
            logging.warn(f"delete_message() failed to find message")
            return

async def set_activity(bot, activity: str):
        """ Sets the bot's activity based on a string.
            Available activities: Playing, Listening to, Watching
            Example: set_activity("Watching in 42 servers") """
        # Generate the discord.Activity based on the first word

        # Only a few of the activity types are supported.
        activities = {
            "Playing": discord.ActivityType.playing,
            "Listening to": discord.ActivityType.listening,
            "Watching": discord.ActivityType.watching,
        }

        # Default to "Playing"
        activity_type = discord.ActivityType.playing

        # CHeck if the activity starts with a supported activity type.
        for activity_name, _activity_type in activities.items():
            if activity.startswith(activity_name):
                activity = activity.strip(activity_name)
                activity_type = _activity_type
                break

        # Set the activity.
        await bot.change_presence(activity=discord.Activity(name=activity, type=activity_type))

async def send_embed(channel, color=None, footer=None, footer_icon=None, subtitle=None,
                        subtext=None, text=None, title=None, thumbnail=None):
    """ Sends a message to a channel, and returns the discord.Message of the sent message.

    If the text is over 2048 characters, subtitle and subtext fields are ignored and the
    message is split up into chunks. The first message will have the title and thumbnail,
    and only the last message will have the footer. Returns the last message sent.
    """
    MAX_MSG_LENGTH = 2048

    # Use a random color if none was given
    if color is None:
        color = random.randint(0, 0xFFFFFF)

    # If the text is short enough to fit into one message,
    # create and send a single embed.
    if text is None or len(text) <= MAX_MSG_LENGTH:
        embed = discord.Embed(color=color)
        if footer is not None:
            if footer_icon is None:
                embed.set_footer(text=footer)
            else:
                embed.set_footer(text=footer, icon_url=footer_icon)
        if subtitle is not None or subtext is not None:
            embed.add_field(name=subtitle, value=subtext, inline=True)
        if thumbnail is not None:
            embed.set_thumbnail(url=thumbnail)
        if title is not None:
            embed.title = title
        if text is not None:
            embed.description = text

        # If this is a ctx, use respond() so the command succeeds and doesn't
        # print "This interaction failed" to the user.
        if type(channel) == discord.commands.context.ApplicationContext:
            response = await channel.respond(embed=embed)
            logging.debug(f"send_embed() -> {response}")
            return

        # Send the single message
        return await channel.send(embed=embed)

    # If the text is too long, it must be broken into chunks.
    message_index = 0
    lines = text.split("\n")
    while lines:
        # Construct the text of this message
        text = ""
        while True:
            if not lines:
                break
            line = lines.pop(0) + '\n'

            # next line fits in this message, add it
            if len(text) + len(line) < MAX_MSG_LENGTH:
                text += line

            # one line is longer than max length of message, split the line and put the rest back
            elif len(line) > MAX_MSG_LENGTH:
                cutoff = MAX_MSG_LENGTH - len(text)
                next_line = line[:cutoff]
                remainder = line[cutoff:-1]
                text += next_line
                lines.insert(0, remainder)
            # message is full - send it
            else:
                lines.insert(0, line)
                break

        embed = discord.Embed(color=color)
        embed.description = text

        # First message in chain - add the title and thumbnail
        if message_index == 0:
            if title is not None:
                embed.title = title
            if thumbnail is not None:
                embed.set_thumbnail(url=thumbnail)
            if subtitle is not None or subtext is not None:
                embed.add_field(name=subtitle, value=subtext, inline=True)
            response = await channel.send(embed=embed)

        # Last message in chain - add the footer.
        if not lines:
            if footer is not None:
                if footer_icon is not None:
                    embed.set_footer(text=footer, icon_url=footer_icon)
                else:
                    embed.set_footer(text=footer)

            # If this is a ctx, use respond() so the command succeeds and doesn't
            # print "This interaction failed" to the user.
            if type(channel) == discord.commands.context.ApplicationContext:
                response = await channel.respond(embed=embed)
            else:
                response = await channel.send(embed=embed)

        message_index = message_index + 1

    # Return the last message sent so reactions can be easily added
    logging.debug(f"send_embed() -> {response}")
    return response

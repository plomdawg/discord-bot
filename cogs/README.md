# cogs

A collection of cogs used by various bots.

## Overview

This directory includes the following cogs:

1. [**Audio Cog**:](#audio-cog) Adds audio file playback functionality.
2. [**Error Handler Cog**:](#error-handler-cog) Captures unhandled errors and notifies a specified user.

## Installation

1. Ensure the `cogs` folder containing `audio.py` and `error_handler.py` is located in the same directory as your bot script.

2. Load the AudioCog and ErrorHandler extensions using the `load_extension` method:

   ```python
   bot.load_extension("cogs.audio")
   bot.load_extension("cogs.error_handler")
   ```

# Cogs

## Audio Cog

The audio cog is adds audio file playback functionality.

## Features

- Load and play audio from URLs.
- Keep audio files in a queue.
- Adjustable playback volume.
- Supports shuffle and repeat modes.

## Usage

Once the cog is installed, you can use the following commands:

### Play an audio track

To play an audio file from a URL in a voice channel, use the `play_url()` method:

```python
await audio_cog.play_url(url="your_audio_file_url", voice_channel=voice_channel)
```

The bot will download the audio file, stick it in a queue, then play it in the user's voice channel.

### Slash commands

The audio cog includes the following slash commands:

- `/volume` - Set the volume for the bot's audio player.

```markdown
/volume 50
```

This sets the volume of the bot's audio player to 50%.

---

## Error Handler Cog

The error handler cog captures unhandled errors that occur during command execution and sends a message to a specified user.

### Setup

Update the user ID in the `error_handler.py` file to your Discord user ID. Locate the following line in the file:

```python
self.plom = self.bot.get_user(163040232701296641)
```

Replace `163040232701296641` with your own Discord user ID.

### Usage

Once installed in your bot, the error handler cog will automatically capture unhandled errors and notify the specified user by sending a private message.

## Example

Here is an example of loading both AudioCog and ErrorHandler in your Discord bot:

```python
import discord
from discord.ext import commands

# Create the discord bot
bot = commands.Bot(command_prefix="!")

# Load the AudioCog
bot.load_extension("cogs.audio")

# Load the ErrorHandler
bot.load_extension("cogs.error_handler")

# Run the bot
bot.run("your_bot_token")
```

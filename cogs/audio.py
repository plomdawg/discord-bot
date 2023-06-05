# Audio utility functions.
import pathlib
import typing
import random
import logging
from discord.ext import commands
import discord
from enum import Enum
import requests

# The directory where audio files are stored.
AUDIO_DIRECTORY = pathlib.Path("audio")
AUDIO_DIRECTORY.mkdir(parents=True, exist_ok=True)


def volume_bar(volume):
    """ Returns an ASCII volume bar for the given volume. 
        volume_bar(25): █████░░░░░░░░░░░░░░░
    """
    length = 20
    filled = int(volume * length / 100)
    unfilled = length - filled
    return "█" * filled + "░" * unfilled


class AudioTrack():
    def __init__(self, name=None, url=None) -> None:
        # The unique name/id of the track.
        self.name = name
        # The URL to the audio file.
        self.url = url
        # Current position in the track.
        self.position = 0
        
        # If the name is not specified, use the last part of the URL.
        if name is None and url is not None:
            self.name = url.split('/')[-1].split('.')[0].strip(".mp3")

    @property
    def downloaded(self) -> bool:
        """ Returns whether the track has been downloaded. """
        return self.path.is_file()

    @property
    def path(self) -> pathlib.Path:
        """ Returns the path to the audio file. """
        return AUDIO_DIRECTORY / f"{self.name}.mp3"
    
    def download(self) -> None:
        """ Downloads the audio file. """
        if not self.downloaded:
            with open(self.path, "wb") as f:
                f.write(requests.get(self.url).content)


class AudioQueue():
    def __init__(self) -> None:
        # The list of tracks in the queue.
        self.tracks: typing.List[AudioTrack] = []
        # The current position in the queue.
        self.position = 0
        # Repeat mode. Can be "none", "one", or "all".
        self.repeat = "none"

    @property
    def current_track(self) -> AudioTrack:
        """ Returns the current track. """
        try:
            return self.tracks[self.position]
        except IndexError:
            return None

    def increment_position(self) -> None:
        """ Increments the position in the queue. """
        # Looping on one track - nothing to do here.
        if self.repeat == "one":
            return

        # Increment the position.
        self.position += 1

        # Loop back to the beginning if we're at the end and repeat is on.
        if self.repeat == "all" and self.position >= len(self.tracks):
            self.position = 0

    def add(self, tracks: typing.List[AudioTrack], play_next=False):
        """ Adds a list of tracks to the queue. """
        for i, track in enumerate(tracks):
            if play_next:
                self.tracks.insert(self.position + 1 + i, track)
            else:
                self.tracks.append(track)

    def clear(self) -> None:
        """ Clears the queue and resets the position. Returns the skipped tracks. """
        cleared_tracks = self.tracks[self.position:]
        self.tracks = []
        self.position = 0
        return cleared_tracks

    def shuffle(self) -> None:
        """ Shuffles the queue beyond the current position. """
        if len(self.tracks) > self.position + 1:
            temp_tracks = self.tracks[self.position + 1:]
            random.shuffle(temp_tracks)
            self.tracks[self.position + 1:] = temp_tracks

class AudioPlayerStatus(Enum):
    PLAYING = 1
    PAUSED = 2
    STOPPED = 3
    CONTINUING = 4

class AudioPlayer():
    def __init__(self, bot, guild) -> None:
        self.bot = bot
        self.guild = guild
        # The queue of tracks to play.
        self.queue = AudioQueue()
        # The voice client to play audio through.
        self.voice_client = None
        # The volume of the audio player.
        self.volume = 0.20  # 20%
        # The current status of the player.
        self.status = AudioPlayerStatus.STOPPED

    async def connect(self, voice_channel: discord.VoiceChannel) -> discord.VoiceClient:
        """ Connects or moves to a voice channel. """
        if self.voice_client:
            await self.voice_client.move_to(voice_channel)
        else:
            self.voice_client = await voice_channel.connect()
                
    async def play(self, voice_channel: discord.VoiceChannel) -> None:
        """ Starts playback in the given voice channel. """
        await self.connect(voice_channel)
        
        # If the player is already playing, do nothing.
        if self.status == AudioPlayerStatus.PLAYING:
            return
        
        # If the player is paused, just resume.
        if self.status == AudioPlayerStatus.PAUSED:
            self.voice_client.resume()
            return
        
        # If there is no track, stop the player.
        if self.queue.current_track is None:
            self.status = AudioPlayerStatus.STOPPED
            return
        
        # Set the status to playing.
        self.status = AudioPlayerStatus.PLAYING

        # Make sure the track is downloaded.
        self.queue.current_track.download()

        # Set up FFMPEG options.
        # -ss skips ahead to the current position in the track.
        # -af loudnorm normalizes the audio.
        ffmpeg_options = f"-ss {self.queue.current_track.position} -af loudnorm=I=-16.0:TP=-1.0"
        
        # Create the audio source.
        audio_source = discord.FFmpegPCMAudio(source=self.queue.current_track.path, options=ffmpeg_options)
        audio_source = discord.PCMVolumeTransformer(audio_source, volume=self.volume)

        def next_track(err=None):
            # Set the status to stopped before moving on.
            self.status = AudioPlayerStatus.STOPPED
            # Move on the the next track in the queue.
            self.queue.increment_position()
            self.bot.loop.create_task(self.play(voice_channel))
        
        # Begin playback.
        self.voice_client.play(audio_source, after=next_track)

    def set_volume(self, volume):
        """ Sets the volume in range [0,100] """
        self.volume = max(min(100, volume), 0)

        # Change current volume if playing.
        if self.voice_client and self.voice_client.source:
            self.voice_client.source.volume = self.volume / 100.0

        return self.volume
    
    async def stop(self) -> None:
        """ Clear the queue and stop playback. """
        self.queue.clear()
        if self.voice_client:
            await self.voice_client.disconnect(force=True)
        self.status = AudioPlayerStatus.STOPPED


class AudioCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.audio = self
        self.audio_players = {}        
    
    def user_in_voice_channel(self, user):
        """ Returns True if the user is in a voice channel. """
        try:
            if user.voice.channel is not None:
                return True
        except AttributeError:
            return False
        return False

    def get_audio_player(self, guild_id: int) -> AudioPlayer:
        """ Returns the audio player for the given guild. """
        if guild_id not in self.audio_players:
            self.audio_players[guild_id] = AudioPlayer(self.bot, guild_id)
        return self.audio_players[guild_id]
    
    async def play_url(self, url, voice_channel) -> None:
        """ Plays audio from a given URL in a voice channel. """
        # Get the audio player for the server.
        audio_player = self.get_audio_player(voice_channel.guild.id)
        
        # Create the audio track.
        audio_track = AudioTrack(url=url)
        
        # Add the track to the queue.
        audio_player.queue.add([audio_track])
        
        # Play the audio.
        await audio_player.play(voice_channel)

    @discord.commands.slash_command(name="volume", description="Set the volume", guild_ids=[708529166693171331, 575720006697091106, 408172061723459584, 886749702102597662])
    async def volume(self, ctx, volume: discord.commands.Option(int, "New volume (0-100) (Default: 20)", required=False)):
        """ Sets the volume for this guild's audio player. """
        audio_player = self.get_audio_player(ctx.guild.id)
        audio_player.set_volume(volume)
        await self._volume(ctx, volume, ctx.author)


def setup(bot):
    logging.info("Loading Audio cog")
    bot.add_cog(AudioCog(bot))
    logging.info("Loaded Audio cog")

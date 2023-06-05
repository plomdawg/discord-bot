import asyncio
import sqlite3
import random
import plomcord
from discord.ext import commands


def get_index_from_query(text):
    """ Splits off the last token in the string if it's a number.
        Example: "dota haha 2" -> ("dota haha", 2)
    """
    try:
        tokens = text.split(' ')
        index = int(tokens[-1]) - 1
        text = ' '.join(tokens[:-1])
    except:
        index = None
    return text, index


class DotaVoiceLinesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.play_lock = False

        print(bot.cogs)

        for cog in bot.cogs:
            print(cog)

        self.dota_wiki = self.bot.get_cog('DotaWikiCog')
        self.database = self.bot.get_cog('Database')
        self.audio = self.bot.get_cog('AudioCog')
        print(self.dota_wiki)
        print(self.database)
        print(self.audio)

        # self.database.create("dota-voice-lines")

        self.db_connection = sqlite3.connect("dota-responses.sqlite")
        self.db_cursor = self.db_connection.cursor()
        self.create_database()

        @self.bot.event
        async def on_message(message):
            """ For every message, we want to do a few things:
                - Check if it's an exact match for a response
                    - If so, play the response
                - Check if the message starts with "dota" (e.g. "dota haha")
                    - If so, play a random response from any hero that contains the text.
                - Check if the message starts with "hero" (e.g. "hero juggernaut")
                    - If so, play a random response from that hero.
                - Check if the message ends with a number (e.g. "dota haha 2")
                    - If so, play the nth response from the query.
            """
            # Ignore bot messages.
            if message.author.bot:
                return

            # Ignore messages if the author is not in a voice channel.
            if not self.audio.user_in_voice_channel(message.author):
                return

            # Check if the message ends in a number.
            text, index = get_index_from_query(message.content)

            # Check if the message is an exact match for a response.
            responses, index = self.get_voice_responses(
                exact_text=text, index=index)
            if responses:
                return await self.respond(message, responses, index)

            # Check if the message starts with "dota" (e.g. "dota haha")
            if text.lower().startswith("dota"):
                # Split off the prefix.
                text = text.split(' ', 1)[1]
                # Get a random response from any hero that contains the text.
                responses, index = self.get_voice_responses(
                    text=text, index=index)
                if responses:
                    return await self.respond(message, responses, index)

            elif text.lower().startswith("hero"):
                # Split off the prefix.
                hero_name = text.split(' ', 1)[1].title()
                # Get a random response from the given hero that contains the text.
                responses, index = self.get_voice_responses(
                    name=hero_name, index=index)
                if responses:
                    return await self.respond(message, responses, index)

    def create_database(self):
        """ Creates the database and loads the json file into it. """
        # Generate the table if needed.
        text_fields = ("name", "responses_url", "url", "text", "thumbnail")
        query = f"CREATE TABLE IF NOT EXISTS responses ({' TEXT, '.join(text_fields)} TEXT)"
        self.db_cursor.execute(query)

        # Populate the responses table.
        for hero in self.dota_wiki.heroes:
            print(
                f"Adding {len(hero.responses)} responses for hero {hero.name}")

            query = f"INSERT or IGNORE INTO responses ({','.join(text_fields)}) VALUES (?,?,?,?,?)"
            data = ([hero.name, hero.responses_url, response.url,
                    response.text, hero.thumbnail] for response in hero.responses)

            self.db_cursor.executemany(query, (data))

    async def respond(self, message, responses, index, forward=True):
        name, response, url, text, thumbnail = responses[index]
        text_channel = message.channel
        text = f"[{text} ({name})]({response})"
        footer = f"voice line {index+1} out of {len(responses)}"
        warning_message = None

        # If the message was sent in my-dudes server,
        # forward the command to the music channel and
        # let the user know the command is being forwarded.
        if forward and message.guild.id == 408172061723459584:
            music_channel = self.bot.get_channel(int(408481491597787136))
            if message.channel != music_channel:
                await message.delete()
                warning = f"{message.author.mention} wrong channel - forwaring to {music_channel.mention}"
                warning_message = await plomcord.send_embed(channel=text_channel, text=warning)
                text_channel = self.bot.get_channel(int(408481491597787136))

        # Respond to the message and play the voice response.
        await plomcord.send_embed(channel=text_channel, text=text, thumbnail=thumbnail, footer=footer)
        await self.audio.play_url(url, message.author.voice.channel)

        # Delete our own message in 30 seconds.
        if warning_message is not None:
            await asyncio.sleep(30)
            await warning_message.delete()

    def get_voice_responses(self, exact_text=None, text=None, index=None, name=None):
        """ Find responses for the given query. """

        # Construct the database operation.
        if exact_text:
            # Match the exact response text.
            operation = f'SELECT * FROM responses WHERE text = "{exact_text}"'
        elif text:
            # Match any response containing the text.
            operation = f'SELECT * FROM responses WHERE text LIKE "%{text}%"'
            # Match the hero name if specified.
            if name:
                operation += f' AND name = "{name}"'
        else:
            operation = f'SELECT * FROM responses WHERE name = "{name}"'

        # Replace elipses with periods.
        operation = operation.replace('…', '...')

        # Fetch the results.
        responses = self.db_cursor.execute(operation).fetchall()

        # Use a random index if not specified.
        if index is None and responses:
            index = random.randint(0, len(responses) - 1)

        return responses, index


def setup(bot):
    print("Loading Dota Voice Lines cog")
    bot.add_cog(DotaVoiceLinesCog(bot))
    print("Loaded Dota Voice Lines cog")
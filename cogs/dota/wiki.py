from discord.ext import commands
import discord
import json

class Ability:
    def __init__(self, data) -> None:
        self.lore = data["lore"]
        self.name = data["name"]
        self.thumbnail = data["thumbnail"]
        self.url = data["url"]

class Hero:
    def __init__(self, data) -> None:
        self.abilities = [Ability(ability) for ability in data["abilities"]]
        self.name = data["_name"]
        self.responses = [VoiceResponse(response) for response in data["responses"]]
        self.thumbnail = data["thumbnail"]
        self.url = data["url"]
        self.responses_url = f"{self.url}/Responses"

class VoiceResponse:
    def __init__(self, data) -> None:
        self.text = data["text"]
        self.url = data["url"]

class Item:
    def __init__(self, data) -> None:
        self.name = data["_name"]
        self.cost = data["gold_cost"]
        self.lore = data["lore"]
        self.thumbnail = data["thumbnail"]
        self.url = data["url"]


class DotaWikiCog(commands.Cog):
    def __init__(self, bot):
        # Store the bot instance so we can access it inside the cog.
        self.bot = bot

        # Load the json file.
        with open("dota_wiki.json", "r") as f:
            self.data = json.load(f)

        self.heroes = [Hero(hero) for hero in self.data["heroes"]]
        self.items = [Item(item) for item in self.data["items"]]
        
    def get_hero(self, name):
        return next((Hero(hero) for hero in self.heroes if hero["_name"] == name), None)

    @discord.commands.slash_command(name="example", description="Example command description")
    async def example(self, ctx, example: discord.commands.Option(int, "Example optional argument", required=False)):
        """ This is the handler for the /example command. """
        print(f"Context: {ctx}")
        print(f"Example: {example}")
        await self.bot.send_embed(ctx, "Example", "Example message")


def setup(bot):
    bot.add_cog(DotaWikiCog(bot))

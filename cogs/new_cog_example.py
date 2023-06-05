from discord.ext import commands
import discord


class ExampleCog(commands.Cog):
    def __init__(self, bot):
        # Store the bot instance so we can access it inside the cog.
        self.bot = bot

    @discord.commands.slash_command(name="example", description="Example command description")
    async def example(self, ctx, example: discord.commands.Option(int, "Example optional argument", required=False)):
        """ This is the handler for the /example command. """
        print(f"Context: {ctx}")
        print(f"Example: {example}")
        await self.bot.send_embed(ctx, "Example", "Example message")


def setup(bot):
    bot.add_cog(ExampleCog(bot))

from discord.ext import commands
from utils.bot import EpicBot
import statcord
import os


class StatcordPost(commands.Cog):
    def __init__(self, bot: EpicBot):
        self.bot = bot
        if not bot.beta:
            self.key = os.environ.get("STATCORD_KEY")
            self.api = statcord.Client(self.bot, self.key)
            self.api.start_loop()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if not self.bot.beta:
            self.api.command_run(ctx)


def setup(bot: EpicBot):
    if not bot.beta:
        bot.add_cog(StatcordPost(bot))

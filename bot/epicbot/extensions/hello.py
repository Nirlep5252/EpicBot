from discord.ext import commands
from bot import EpicBot


class Hello(commands.Cog):
    def __init__(self, bot: EpicBot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def hello(self, ctx: commands.Context) -> None:
        await ctx.reply("Hello!")


async def setup(bot: EpicBot) -> None:
    await bot.add_cog(Hello(bot))

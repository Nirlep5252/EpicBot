from discord.ext import commands
import discord
from typing import Optional


class SlashCogTesting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roleicon(self, ctx: commands.Context, user: Optional[discord.User] = None):
        user = user or ctx.author
        await ctx.reply(user.top_role)


def setup(bot):
    bot.add_cog(SlashCogTesting(bot))

from discord.ext import commands
from handlers.slash import slash_command, SlashContext
import discord


class SlashCogTesting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[746202728031584358])
    async def slash(self, ctx: SlashContext, arg: discord.Member):
        await ctx.reply(arg, ephemeral=True)


def setup(bot):
    bot.add_cog(SlashCogTesting(bot))

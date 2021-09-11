from discord.ext import commands
from handlers.slash import slash_command
import discord


class SlashCogTesting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @slash_command(guild_ids=[746202728031584358])
    # async def slash(self, ctx: discord.Interaction, arg: str):
    #     await ctx.reply(arg, ephermal=True)


def setup(bot):
    bot.add_cog(SlashCogTesting(bot))

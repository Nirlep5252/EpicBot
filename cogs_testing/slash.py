from discord.ext import commands
from handlers.slash import slash_command, SlashContext, SlashCommandOption, SlashCommandChoice
import discord


class SlashCogTesting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[746202728031584358], help="Slap some annoying kid.")
    async def slap(self, ctx: SlashContext, user: discord.Member = None):
        await ctx.reply(f"You slapped {(user or ctx.author).mention}", ephemeral=True)

    @slash_command(guild_ids=[746202728031584358], help="Pick something.")
    async def pick(self, ctx: SlashContext, something: SlashCommandOption(
        name="something",
        type=3,
        description="Pick something.",
        required=True,
        choices=[SlashCommandChoice(name='amogus', value='sus'), SlashCommandChoice(name='susu', value='idk ajajja')]
    )):
        await ctx.reply(f"You picked {something}", ephemeral=True)


def setup(bot):
    bot.add_cog(SlashCogTesting(bot))

from discord.ext import commands
from handler import slash_command, InteractionContext, SlashCommandOption, SlashCommandChoice, user_command, message_command
import discord


class SlashCogTesting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=[746202728031584358], help="Slap some annoying kid.")
    async def slap(self, ctx: InteractionContext, user: discord.Member = None):
        await ctx.reply(f"You slapped {(user or ctx.author).mention}", ephemeral=True)

    @slash_command(guild_ids=[746202728031584358], help="Pick something.")
    async def pick(self, ctx: InteractionContext, something: SlashCommandOption(
        name="something",
        type=3,
        description="Pick something.",
        required=True,
        choices=[SlashCommandChoice(name='amogus', value='sus'), SlashCommandChoice(name='susu', value='idk ajajja')]
    )):
        await ctx.reply(f"You picked {something}", ephemeral=True)

    @user_command(guild_ids=[746202728031584358])
    async def sex(self, ctx: InteractionContext):
        if ctx.target == ctx.author:
            return await ctx.reply("Imagine having sex with yourself...", ephemeral=True)
        await ctx.reply(f"You can't have sex with {ctx.target.mention}", ephemeral=True)

    @message_command(guild_ids=[746202728031584358])
    async def cute(self, ctx: InteractionContext):
        await ctx.reply(f"This [message]({ctx.target.jump_url}) is very cute, but you are cuter 👀", ephemeral=True)


def setup(bot):
    bot.add_cog(SlashCogTesting(bot))

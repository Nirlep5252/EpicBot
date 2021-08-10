from typing import List
from discord import Role, Reaction, Member, Message, PartialEmoji
from discord.ext.commands import Context


async def prepare_emojis_and_roles(ctx: Context, roles: List[Role], message: Message):

    output = {}

    def check(reaction: Reaction, user: Member):
        return user == ctx.author and reaction.message == message

    for role in roles:
        embed = message.embeds[0]
        embed.clear_fields()
        embed.add_field(name=f"Role ({roles.index(role) + 1}/{len(roles)}):", value=role.mention, inline=False)
        await message.edit(embed=embed)

        reaction, user = await ctx.bot.wait_for("reaction_add", check=check)

        if isinstance(reaction.emoji, PartialEmoji):
            await ctx.send("Please only use the emojis that I can access.", delete_after=5)
            await message.remove_reaction(reaction, user)
            return await prepare_emojis_and_roles(ctx, roles, message)

        output.update({
            str(role.id): str(reaction.emoji)
        })

    await message.clear_reactions()
    return output

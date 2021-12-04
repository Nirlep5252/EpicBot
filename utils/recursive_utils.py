from typing import List
from discord import Role, Reaction, Member, Message, PartialEmoji
from discord.ext.commands import Context
from asyncio import TimeoutError
from utils.embed import success_embed


async def prepare_emojis_and_roles(ctx: Context, roles: List[Role], message: Message):
    embed = success_embed(
         f"{len(roles)} Roles found!",
        f"I have found **{len(roles)}** in your message.\n\n{' '.join(role.mention for role in roles)}\n\nNow you need to react to this message with the corresponding emojis for the rolemenu to be complete!"
    )
    await message.edit(embed=embed)
    output = {}

    def check(reaction: Reaction, user: Member):
        return user == ctx.author and reaction.message == message

    for role in roles:
        embed.clear_fields()
        embed.add_field(name=f"Role ({roles.index(role) + 1}/{len(roles)}):", value=role.mention, inline=False)
        await message.edit(embed=embed)

        try:
            reaction, user = await ctx.bot.wait_for("reaction_add", check=check, timeout=60)
        except TimeoutError:
            await message.edit(content="You didn't respond in time!", embed=None, view=None)
            return None

        if isinstance(reaction.emoji, PartialEmoji):
            await ctx.send("Please only use the emojis that I can access.", delete_after=5)
            await message.remove_reaction(reaction, user)
            return await prepare_emojis_and_roles(ctx, roles, message)

        output.update({
            str(role.id): str(reaction.emoji)
        })

    await message.clear_reactions()
    return output

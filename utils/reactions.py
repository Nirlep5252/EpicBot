from discord import TextChannel
from discord.ext.commands import Context
from utils.ui import ButtonSelfRoleView, DropDownSelfRoleView
from utils.embed import success_embed


async def prepare_rolemenu(ctx: Context, stuff: dict, channel: TextChannel, type_: str = 'reaction', msg_id=None, edit: bool = False) -> int:
    text = ""
    for role_id, emoji in stuff.items():
        role = ctx.guild.get_role(int(role_id))
        if role is not None:
            text += f"{emoji} - {role.mention}\n"
    embed = success_embed(
        "Rolemenu - Get your roles!",
        text
    )
    if type_ == 'reaction':
        if msg_id is None:
            msg = await channel.send(embed=embed)
        else:
            msg = await channel.fetch_message(int(msg_id))
        for role_id, emoji in stuff.items():
            await msg.add_reaction(emoji)
        return msg.id

    if type_ == 'button':
        view = ButtonSelfRoleView(ctx.guild, stuff)
    elif type_ == 'dropdown':
        view = DropDownSelfRoleView(ctx.guild, stuff)

    if not edit:
        msg = await channel.send(embed=embed, view=view)
    else:
        msg = await channel.fetch_message(int(msg_id))
        await msg.edit(embed=embed, view=view)
    return msg.id

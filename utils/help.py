"""
Copyright 2021 Nirlep_5252_

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import discord
import datetime
from discord.ext import commands
from utils.embed import error_embed
from config import (
    EMOJIS, EMOJIS_FOR_COGS, MAIN_COLOR,
    EMPTY_CHARACTER, WEBSITE_LINK, SUPPORT_SERVER_LINK
)


async def get_cog_help(ctx: commands.Context, cog_name: str) -> discord.Embed:
    if cog_name == "nsfw" and not ctx.channel.is_nsfw():
        return error_embed(
            f"{EMOJIS['tick_no']} Go away horny!",
            "Please go to a **NSFW** channel to see the commands."
        )
    cog = ctx.bot.get_cog(cog_name)
    return discord.Embed(
        title=f"{cog_name.title()} Category",
        description="**Here are all the commands:**\n\n" + "\n".join([f"{EMOJIS['cmd_arrow']} `{e.name}` • {e.help}" for e in cog.get_commands()]),
        color=MAIN_COLOR
    ).set_thumbnail(url=ctx.bot.user.display_avatar.url
    ).add_field(name=EMPTY_CHARACTER, value=f"[Invite EpicBot]({WEBSITE_LINK}/invite) | [Vote EpicBot]({WEBSITE_LINK}/vote) | [Support Server]({SUPPORT_SERVER_LINK})", inline=False)


async def get_command_help(ctx: commands.Context, command_name: str) -> discord.Embed:
    command = ctx.bot.get_command(command_name)
    if command.cog_name == "nsfw" and not ctx.channel.is_nsfw():
        return error_embed(
            f"{EMOJIS['tick_no']} Go away horny!",
            "Please go to a **NSFW** channel to see the command."
        )
    return discord.Embed(
        title=f"{command_name.title()} Help",
        description=f"""
{command.help}

**Usage:**
```
{ctx.clean_prefix}{command.name} {' '.join(['<' + str(param) + '>' for param in command.clean_params])}
```
**Aliases:** {','.join(['`' + str(alias) + '`' for alias in command.aliases])}
**Cooldown:** {0 if command._buckets._cooldown == None else command._buckets._cooldown.per} seconds
                    """,
        color=MAIN_COLOR,
        timestamp=datetime.datetime.utcnow()
    ).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url
    ).set_author(name=ctx.bot.user.name, icon_url=ctx.bot.user.display_avatar.url
    ).set_thumbnail(url=ctx.bot.user.display_avatar.url
    ).add_field(name=EMPTY_CHARACTER, value=f"[Invite EpicBot]({WEBSITE_LINK}/invite) | [Vote EpicBot]({WEBSITE_LINK}/vote) | [Support Server]({SUPPORT_SERVER_LINK})", inline=False)


async def get_bot_help(ctx: commands.Context, mapping) -> discord.Embed:
    return discord.Embed(
        title="All the categories:",
        description="\n".join(
            [f"{EMOJIS_FOR_COGS[cog.qualified_name]} • **{cog.qualified_name.title()}** [ `{len(cmds)}` ]" for cog, cmds in mapping.items() if cog is not None and cog.qualified_name == cog.qualified_name.lower()]),
        color=MAIN_COLOR,
        timestamp=datetime.datetime.utcnow()
    ).set_author(name=ctx.bot.user.name, icon_url=ctx.bot.user.display_avatar.url
    ).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url
    ).add_field(name="Links:", value=f"""
[Dashboard]({WEBSITE_LINK}) | [Support]({SUPPORT_SERVER_LINK}) | [Invite]({WEBSITE_LINK}/invite) | [Winlep](https://www.winlep.cf/)
    """, inline=False)


async def get_commands_list(ctx: commands.Context, mapping) -> discord.Embed:
    embed = discord.Embed(
        title="All the commands:",
        description=f"Please use `{ctx.clean_prefix}help <command>` for more info.",
        color=MAIN_COLOR,
        timestamp=datetime.datetime.utcnow()
    ).set_author(name=ctx.bot.user.name, icon_url=ctx.bot.user.display_avatar.url
    ).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)

    for cog, commands_ in mapping.items():
        if cog is not None and cog.qualified_name == cog.qualified_name.lower():
            embed.add_field(
                name=f"{EMOJIS_FOR_COGS[cog.qualified_name]} • {cog.qualified_name.title()}",
                value=", ".join([f"`{command.name}`" for command in commands_]),
                inline=False
            )

    embed.add_field(name="Links:", value=f"""
[Dashboard]({WEBSITE_LINK}) | [Support]({SUPPORT_SERVER_LINK}) | [Invite]({WEBSITE_LINK}/invite)
    """, inline=False)

    return embed


class HelpSelect(discord.ui.Select):
    def __init__(self, ctx: commands.Context, options):
        super().__init__(placeholder="Please select a category.", options=options)
        self.ctx = ctx

    async def callback(self, i: discord.Interaction):
        self.view.children[0].disabled = False
        embed = await get_cog_help(self.ctx, self.values[0])
        await i.message.edit(embed=embed, view=self.view)


class HelpMenu(discord.ui.View):
    def __init__(self, ctx: commands.Context, mapping):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.mapping = mapping

    @discord.ui.button(label="Home", emoji="🏠", style=discord.ButtonStyle.blurple, disabled=True)
    async def home(self, button: discord.ui.Button, interaction: discord.Interaction):
        for item in self.children:
            item.disabled = False
        button.disabled = True
        embed = await get_bot_help(self.ctx, self.mapping)
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label="Command List", emoji="📃", style=discord.ButtonStyle.blurple)
    async def commands_list(self, button: discord.ui.Button, interaction: discord.Interaction):
        for item in self.children:
            item.disabled = False
        button.disabled = True
        embed = await get_commands_list(self.ctx, self.mapping)
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label="Delete Menu", emoji='🛑', style=discord.ButtonStyle.danger)
    async def delete_menu(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message("Not your command ._.", ephemeral=True)


class EpicBotHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = await get_bot_help(self.context, mapping)
        view = HelpMenu(self.context, mapping)
        select = HelpSelect(
            self.context,
            [discord.SelectOption(
                label=cog.qualified_name.title(),
                emoji=EMOJIS_FOR_COGS[cog.qualified_name],
                value=cog.qualified_name,
                description=cog.description
            ) for cog, cmds in mapping.items() if cog is not None and cog.qualified_name == cog.qualified_name.lower()]
        )
        view.add_item(select)
        await self.context.reply(embed=embed, view=view)

    async def send_cog_help(self, cog):
        return await self.context.reply(embed=await get_cog_help(self.context, cog.qualified_name))

    async def send_command_help(self, command):
        return await self.context.reply(embed=await get_command_help(self.context, command.name))

    async def send_error_message(self, error):
        return await self.context.reply(embed=error_embed(f"{EMOJIS['tick_no']} Error", error))

    async def send_group_help(self, group):
        return await super().send_group_help(group)

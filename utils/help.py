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
from config import MAIN_COLOR, EMOJIS_FOR_COGS, EMOJIS, EMPTY_CHARACTER, WEBSITE_LINK, SUPPORT_SERVER_LINK
from utils.embed import error_embed


async def get_cog_help(cog, context):
    cog = context.bot.get_cog(cog)
    if cog.qualified_name == 'nsfw' and not context.channel.is_nsfw():
        return error_embed(
            f"{EMOJIS['tick_no']} Go away horny!",
            "Please go to a **NSFW** channel to see the commands."
        )

    embed = discord.Embed(
        title=f"{cog.qualified_name.title()} Category",
        color=MAIN_COLOR
    ).set_thumbnail(url=context.bot.user.display_avatar.url
                    ).add_field(name=EMPTY_CHARACTER, value=f"[Invite EpicBot]({WEBSITE_LINK}/invite) | [Vote EpicBot]({WEBSITE_LINK}/vote) | [Support Server]({SUPPORT_SERVER_LINK})", inline=False)

    nice = ""
    cmds = cog.get_commands()

    for e in cmds:
        nice += f"`{e.name}` - {e.help}\n"

    embed.description = f"To get detailed help, please use `{context.clean_prefix}help <cmd>`\n\n**Commands:**\n{nice}"

    return embed


class EpicBotHelpSelect(discord.ui.Select):
    def __init__(self, placeholder, options, ctx):
        super().__init__(
            placeholder=placeholder,
            options=options
        )
        self.ctx = ctx

    async def callback(self, i):
        await i.response.send_message(embed=await get_cog_help(
            self.values[0], self.ctx
        ), ephemeral=True)


class EpicBotHelp(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Help Command",
            description="Hello, I am a simple, multipurpose Discord bot, built to make your Discord life easier!\n\n**Select a category:**",
            color=MAIN_COLOR,
            timestamp=datetime.datetime.utcnow()
        ).set_thumbnail(url=self.context.bot.user.display_avatar.url
        ).set_author(name=self.context.bot.user.name, icon_url=self.context.bot.user.display_avatar.url
        ).set_footer(text=f"Requested by {self.context.author}", icon_url=self.context.author.display_avatar.url)

        view_ui = discord.ui.View(timeout=None)
        options = []
        for cog, cmds in mapping.items():
            if cog is not None and cog.qualified_name.lower() == cog.qualified_name:
                embed.add_field(
                    name=f"{EMOJIS_FOR_COGS[cog.qualified_name]}  {cog.qualified_name.title()} [ `{len(cmds)}` ]",
                    value=cog.description,
                    inline=False
                )
                options.append(discord.SelectOption(
                    label=cog.qualified_name.title(),
                    description=cog.description,
                    value=cog.qualified_name,
                    emoji=EMOJIS_FOR_COGS[cog.qualified_name]
                ))
        select = EpicBotHelpSelect(
            placeholder="Select a category.",
            options=options,
            ctx=self.context
        )
        view_ui.add_item(select)
        view_ui.add_item(discord.ui.Button(
            style=discord.ButtonStyle.url,
            url=WEBSITE_LINK,
            label="Dashboard",
        ))
        view_ui.add_item(discord.ui.Button(
            style=discord.ButtonStyle.url,
            url=SUPPORT_SERVER_LINK,
            label="Support Server",
        ))
        view_ui.add_item(discord.ui.Button(
            style=discord.ButtonStyle.url,
            url=f"{WEBSITE_LINK}/vote",
            label="Vote",
        ))

        await self.context.reply(embed=embed, view=view_ui)

    async def send_command_help(self, command):
        if command.cog_name == 'nsfw' and not self.context.channel.is_nsfw():
            return await self.context.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Go away horny!",
                "Please go to a **NSFW** channel to see the command."
            ))
        uwu = ""
        aliases = ""
        for cancer in command.clean_params:
            uwu += f"<{cancer}> "
        for alias in command.aliases:
            aliases += f"`{alias}` "
        embed = discord.Embed(
            title=f"{command.name.title()} Help",
            description=f"""
{command.help}

**Usage:**
```
{self.context.clean_prefix}{command.name} {uwu}
```
**Aliases:** {aliases if len(aliases) > 0 else "None"}
**Cooldown:** {0 if command._buckets._cooldown == None else command._buckets._cooldown.per} seconds
                        """,
            color=MAIN_COLOR,
            timestamp=datetime.datetime.utcnow()
        ).set_footer(text=f"Requested by {self.context.author}", icon_url=self.context.author.display_avatar.url
        ).set_author(name=self.context.bot.user.name, icon_url=self.context.bot.user.display_avatar.url
        ).set_thumbnail(url=self.context.bot.user.display_avatar.url
        ).add_field(name=EMPTY_CHARACTER, value=f"[Invite EpicBot]({WEBSITE_LINK}/invite) | [Vote EpicBot]({WEBSITE_LINK}/vote) | [Support Server]({SUPPORT_SERVER_LINK})", inline=False)
        await self.context.reply(embed=embed)

    async def send_cog_help(self, cog):
        await self.context.reply(embed=await get_cog_help(cog.qualified_name, self.context))

    async def send_group_help(self, group):
        pass

    async def send_error_message(self, error):
        await self.context.reply(embed=error_embed(f"{EMOJIS['tick_no']} Error!", error))

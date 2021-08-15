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
    ).set_thumbnail(url=ctx.bot.user.avatar.url
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
{ctx.clean_prefix}{command.name} {''.join(['<' + str(param) + '>' for param in command.clean_params])}
```
**Aliases:** {','.join(['`' + str(alias) + '`' for alias in command.aliases])}
**Cooldown:** {0 if command._buckets._cooldown == None else command._buckets._cooldown.per} seconds
                    """,
        color=MAIN_COLOR,
        timestamp=datetime.datetime.utcnow()
    ).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url
    ).set_author(name=ctx.bot.user.name, icon_url=ctx.bot.user.avatar.url
    ).set_thumbnail(url=ctx.bot.user.avatar.url
    ).add_field(name=EMPTY_CHARACTER, value=f"[Invite EpicBot]({WEBSITE_LINK}/invite) | [Vote EpicBot]({WEBSITE_LINK}/vote) | [Support Server]({SUPPORT_SERVER_LINK})", inline=False)


async def get_bot_help(ctx: commands.Context) -> discord.Embed:
    return discord.Embed(color=MAIN_COLOR, timestamp=datetime.datetime.utcnow()
        ).set_author(name=ctx.bot.user.name, icon_url=ctx.bot.user.avatar.url
        ).set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)


class HelpMenu(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=None)
        self.ctx = ctx

    @discord.ui.button(label="Home", emoji="🏠", style=discord.ButtonStyle.blurple)
    async def home():
        pass


class EpicBotHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        pass

    async def send_cog_help(self, cog):
        return super().send_cog_help(cog)

    async def send_command_help(self, command):
        return super().send_command_help(command)

    async def send_error_message(self, error):
        return super().send_error_message(error)

    async def send_group_help(self, group):
        return super().send_group_help(group)

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

from handler.app_commands import InteractionContext
from utils.time import datetime_to_seconds
import discord
import time
import datetime
import pygit2
import itertools
from discord.utils import escape_markdown
from discord.ext import commands

from config import (
    EMOJIS_FOR_COGS, MAIN_COLOR, ORANGE_COLOR,
    EMOJIS, WEBSITE_LINK, SUPPORT_SERVER_LINK,
    INVITE_BOT_LINK, start_time
)
from utils.embed import error_embed
from utils.bot import EpicBot
from utils.ui import BasicView
from handler import user_command
from typing import List, Optional, Union


def format_commit(commit: pygit2.Commit) -> str:
    # CREDITS: https://github.com/Rapptz/RoboDanny
    short, _, _ = commit.message.partition('\n')
    short_sha2 = commit.hex[0:6]
    commit_tz = datetime.timezone(
        datetime.timedelta(minutes=commit.commit_time_offset))
    commit_time = datetime.datetime.fromtimestamp(
        commit.commit_time).astimezone(commit_tz)

    offset = f'<t:{int(commit_time.astimezone(datetime.timezone.utc).timestamp())}:R>'
    return f'[`{short_sha2}`](https://github.com/DeveloperJosh/MailHook/commit/{commit.hex}) {short} ({offset})'


def get_commits(count: int = 3):
    # CREDITS: https://github.com/Rapptz/RoboDanny
    repo = pygit2.Repository('.git')
    commits = list(itertools.islice(
        repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL), count))
    return '\n'.join(format_commit(commit) for commit in commits)


class UserinfoView(BasicView):

    def __init__(self, ctx: commands.Context, timeout: Optional[int] = None, embeds: List[discord.Embed] = None):
        super().__init__(ctx, timeout=timeout)
        self.embeds = embeds or []

    @discord.ui.button(label="Info", emoji=EMOJIS_FOR_COGS['info'], style=discord.ButtonStyle.blurple, disabled=True)
    async def info(self, b: discord.ui.Button, interaction: discord.Interaction):
        self.susu(b)
        await interaction.message.edit(embed=self.embeds[0], view=self)

    @discord.ui.button(label="Roles", emoji='<:role:890807676697710622>', style=discord.ButtonStyle.blurple)
    async def roles(self, b: discord.ui.Button, interaction: discord.Interaction):
        self.susu(b)
        await interaction.message.edit(embed=self.embeds[1], view=self)

    @discord.ui.button(label="Permissions", emoji='🛠️', style=discord.ButtonStyle.blurple)
    async def permissions(self, b: discord.ui.Button, interaction: discord.Interaction):
        self.susu(b)
        await interaction.message.edit(embed=self.embeds[2], view=self)

    def susu(self, b):
        for i in self.children:
            i.disabled = False
        b.disabled = True


class info(commands.Cog, description="Statistic related commands"):
    def __init__(self, client: EpicBot):
        self.client = client

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(help="Get COVID-19 stats about any country.")
    async def covid(self, ctx, *, country=None):
        PREFIX = ctx.clean_prefix
        if country is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed("Invalid Usage!", f"Please use it like this: `{PREFIX}covid <country>`"))

        try:
            async with self.client.session.get(f"https://coronavirus-19-api.herokuapp.com/countries/{country.lower()}") as r:
                response = await r.json()
        except Exception:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed("Error!", f"Couldn't find COVID-19 stats about `{country}`."))

        country = response['country']
        total_cases = response['cases']
        today_cases = response['todayCases']
        total_deaths = response['deaths']
        today_deaths = response['todayDeaths']
        recovered = response['recovered']
        active_cases = response['active']
        critical_cases = response['critical']
        total_tests = response['totalTests']
        cases_per_one_million = response['casesPerOneMillion']
        deaths_per_one_million = response['deathsPerOneMillion']
        tests_per_one_million = response['testsPerOneMillion']

        embed = discord.Embed(
            title=f"COVID-19 Status of {country}",
            description="This information isn't always live, so it may not be accurate.",
            color=ORANGE_COLOR
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")

        embed.add_field(
            name="Total",
            value=f"""
```yaml
Total Cases: {total_cases}
Total Deaths: {total_deaths}
Total Tests: {total_tests}
```
            """,
            inline=False
        )
        embed.add_field(
            name="Today",
            value=f"""
```yaml
Today Cases: {today_cases}
Today Deaths: {today_deaths}
```
            """,
            inline=False
        )
        embed.add_field(
            name="Other",
            value=f"""
```yaml
Recovered: {recovered}
Active Cases: {active_cases}
Critical Cases: {critical_cases}
```
            """,
            inline=False
        )
        embed.add_field(
            name="Per One Million",
            value=f"""
```yaml
Cases Per One Million: {cases_per_one_million}
Deaths Per One Million: {deaths_per_one_million}
Tests Per One Million: {tests_per_one_million}
```
            """,
            inline=False
        )

        await ctx.message.reply(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(help="Get info about a role.")
    async def roleinfo(self, ctx: commands.Context, role: discord.Role = None):
        prefix = ctx.clean_prefix
        if role is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please mention a role to get info about.\nCorrect Usage: `{prefix}roleinfo @role`"
            ))
        embed = discord.Embed(
            title=f"{EMOJIS['tick_yes']} Role Information",
            color=role.color
        )
        embed.add_field(
            name="Basic Info:",
            value=f"""
```yaml
Name: {role.name}
ID: {role.id}
Position: {role.position}
Color: {str(role.color)[1:]}
Hoisted: {role.hoist}
Members: {len(role.members)}
```
            """,
            inline=False
        )
        something = ""
        for permission in role.permissions:
            a, b = permission
            a = ' '.join(a.split('_')).title()
            hmm = '+' if b else '-'
            something += hmm + ' ' + a + '\n'
        embed.add_field(
            name="Permissions:",
            value=f"```diff\n{something}\n```",
            inline=False
        )
        await ctx.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Get info about users!")
    @user_command(name="Userinfo")
    async def userinfo(self, ctx: Union[commands.Context, InteractionContext], user: Optional[Union[discord.Member, discord.User]] = None):
        if isinstance(ctx, commands.Context):
            user = user or ctx.author
        else:
            user = user or ctx.target

        _user = await self.client.fetch_user(user.id)  # to get the banner

        embed = discord.Embed(
            color=_user.accent_color or user.color or MAIN_COLOR,
            description=f"{user.mention} {escape_markdown(str(user))} ({user.id})",
            timestamp=datetime.datetime.utcnow()
        ).set_author(name=user, icon_url=user.display_avatar.url
        ).set_footer(text=self.client.user.name, icon_url=self.client.user.display_avatar.url
        ).set_thumbnail(url=user.display_avatar.url
        )
        if _user.banner is not None:
            embed.set_image(url=_user.banner.url)

        embed1 = embed.copy()
        c = str(int(user.created_at.astimezone(datetime.timezone.utc).timestamp()))
        j = str(int(user.joined_at.astimezone(datetime.timezone.utc).timestamp())) if isinstance(user, discord.Member) else None
        embed1.add_field(
            name="Account Info:",
            value=f"""
**Username:** {escape_markdown(user.name)}
**Nickname:** {escape_markdown(user.display_name)}
**ID:** {user.id}
            """,
            inline=False
        )
        embed1.add_field(
            name="Age Info:",
            value=f"""
**Created At:** <t:{c}:F> <t:{c}:R>
**Joined At:** {'<t:' + j + ':F> <t:' + j + ':R>' if j is not None else 'Not in the server.'}
            """,
            inline=False
        )
        embed1.add_field(
            name="URLs:",
            value=f"""
**Avatar URL:** [Click Me]({user.display_avatar.url})
**Guild Avatar URL:** [Click Me]({(user.guild_avatar.url if user.guild_avatar is not None else user.display_avatar.url) if isinstance(user, discord.Member) else user.display_avatar.url})
**Banner URL:** {'[Click Me](' + _user.banner.url + ')' if _user.banner is not None else 'None'}
            """,
            inline=False
        )

        embed2 = embed.copy()
        r = (', '.join(role.mention for role in user.roles[1:][::-1]) if len(user.roles) > 1 else 'No Roles.') if isinstance(user, discord.Member) else 'Not in server.'
        embed2.add_field(
            name="Roles:",
            value=r if len(r) <= 1024 else r[0:1006] + ' and more...',
            inline=False
        )

        embed3 = embed.copy()
        embed3.add_field(
            name="Permissions:",
            value=', '.join([perm.replace('_', ' ').title() for perm, value in iter(user.guild_permissions) if value]) if isinstance(user, discord.Member) else 'Not in server.',
            inline=False
        )
        embeds = [embed1, embed2, embed3]
        v = UserinfoView(ctx, None, embeds)
        await ctx.reply(embed=embed1, view=v)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Get info about the server!")
    async def serverinfo(self, ctx: commands.Context):
        guild: discord.Guild = ctx.guild
        embed = discord.Embed(
            title=f"{EMOJIS_FOR_COGS['info']} Server Information",
            description=f"Description: {guild.description}",
            color=MAIN_COLOR
        ).set_author(
            name=guild.name,
            icon_url=guild.me.display_avatar.url if guild.icon is None else guild.icon.url
        ).set_footer(text=f"ID: {guild.id}")
        if guild.icon is not None:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(
            name="Basic Info:",
            value=f"""
**Owner:** <@{guild.owner_id}>
**Created At:** <t:{round(time.time() - (datetime_to_seconds(guild.created_at) - time.time()))}:F>
**Region:** {str(guild.region).title()}
**System Channel:** {"None" if guild.system_channel is None else guild.system_channel.mention}
**Verification Level:** {str(guild.verification_level).title()}
            """,
            inline=False
        )
        embed.add_field(
            name="Members Info:",
            value=f"""
**Members:** `{len(guild.members)}`
**Humans:** `{len(list(filter(lambda m: not m.bot, guild.members)))}`
**Bots:** `{len(list(filter(lambda m: m.bot, guild.members)))}`
            """,
            inline=True
        )
        embed.add_field(
            name="Channels Info:",
            value=f"""
**Categories:** `{len(guild.categories)}`
**Text Channels:** `{len(guild.text_channels)}`
**Voice Channels:** `{len(guild.voice_channels)}`
**Threads:** `{len(guild.threads)}`
            """,
            inline=True
        )
        embed.add_field(
            name="Other Info:",
            value=f"""
**Roles:** `{len(guild.roles)}`
**Emojis:** `{len(guild.emojis)}`
**Stickers:** `{len(guild.stickers)}`
                """
        )
        if guild.features:
            embed.add_field(
                name="Features:",
                value=', '.join([feature.replace('_', ' ').title() for feature in guild.features]),
                inline=False
            )
        if guild.banner is not None:
            embed.set_image(url=guild.banner.url)

        return await ctx.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['av', 'pfp'], help="Get the user's avatar")
    async def avatar(self, ctx: commands.Context, user: Optional[Union[discord.Member, discord.User]] = None):
        user = user or ctx.author
        embed = discord.Embed(
            title=f"Avatar of {escape_markdown(str(user))}",
            color=user.color,
            description=f'Link as: [`png`]({user.display_avatar.replace(format="png").url}) | [`jpg`]({user.display_avatar.replace(format="jpg").url}) | [`webp`]({user.display_avatar.replace(format="webp").url})'
        ).set_image(url=user.display_avatar.url)
        await ctx.message.reply(embed=embed)

#     @commands.cooldown(1, 60, commands.BucketType.user)
#     @commands.command(aliases=['stats'], help="Get info about me!")
#     async def botinfo(self, ctx):
#         msg = await ctx.message.reply(embed=discord.Embed(title=f"Loading... {EMOJIS['loading']}"))
#         embed = discord.Embed(
#             title="Information About Me!",
#             description="I am a simple, multipurpose Discord bot, built to make ur Discord life easier!",
#             color=MAIN_COLOR
#         ).set_thumbnail(url=self.client.user.display_avatar.url)
#         embed.add_field(
#             name="Stats",
#             value=f"""
# ```yaml
# Servers: {len(self.client.guilds)}
# Users: {len(set(self.client.get_all_members()))}
# Total Commands: {len(self.client.commands)}
# Uptime: {str(datetime.timedelta(seconds=int(round(time.time()-start_time))))}
# Version: V2 Rewrite
# ```
#             """,
#             inline=False
#         )
# #         async with self.client.session.get("https://statcord.com/logan/stats/751100444188737617") as r:
# #             ah_yes = await r.json()
# #         embed.add_field(
# #             name="Statcord Stats",
# #             value=f"""
# # ```yaml
# # Commands Ran Today: {ah_yes['data'][::-1][0]['commands']}
# # Most Used Command: {ah_yes['data'][::-1][0]['popular'][0]['name']} - {ah_yes['data'][::-1][0]['popular'][0]['count']} uses
# # Memory Usage: {'%.1f' % float(int(ah_yes['data'][::-1][0]['memactive'])/1000000000)} GB / {'%.1f' % float(int(psutil.virtual_memory().total)/1000000000)} GB
# # Memory Load: {ah_yes['data'][::-1][0]['memload']}%
# # CPU Load: {ah_yes['data'][::-1][0]['cpuload']}%
# # ```
# #             """,
# #             inline=False
# #         )
#         embed.add_field(
#             name="Links",
#             value=f"""
# - [Dashboard]({WEBSITE_LINK})
# - [Support Server]({SUPPORT_SERVER_LINK})
# - [Invite EpicBot]({INVITE_BOT_LINK})
# - [Vote EpicBot]({WEBSITE_LINK}/vote)
#             """,
#             inline=True
#         )
#         embed.add_field(
#             name="Owner Info",
#             value="""
# Made by: **[Nirlep\_5252\_](https://discord.com/users/558861606063308822)**
#             """,
#             inline=True
#         )

#         await msg.edit(embed=embed)

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(aliases=['stats'], help="Get info about me!")
    async def botinfo(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Info about me!",
            description="A simple multipurpose Discord bot.",
            color=MAIN_COLOR,
            timestamp=datetime.datetime.utcnow()
        ).add_field(
            name="Stats:",
            value=f"""
**Servers:** {len(self.client.guilds)}
**Users:** {len(self.client.users)}
**Commands:** {len(self.client.commands)}
**Uptime:** {str(datetime.timedelta(seconds=int(round(time.time()-start_time))))}
**Version:** V2 Rewrite
            """,
            inline=True
        ).add_field(
            name="Links:",
            value=f"""
- [Website]({WEBSITE_LINK})
- [Support]({SUPPORT_SERVER_LINK})
- [Invite]({INVITE_BOT_LINK})
- [Vote]({WEBSITE_LINK}/vote)
- [Github](https://github.com/nirlep5252/epicbot)
            """,
            inline=True
        ).set_footer(text=self.client.user.name, icon_url=self.client.user.display_avatar.url
        ).set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar.url
        ).set_thumbnail(url=self.client.user.display_avatar.url)
        try:
            embed.add_field(
                name="Latest Commits:",
                value=get_commits(),
                inline=False
            )
        except Exception:
            pass
        await ctx.reply(embed=embed)


def setup(client):
    client.add_cog(info(client))

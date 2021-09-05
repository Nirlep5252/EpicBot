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

from utils.time import datetime_to_seconds
import discord
import time
import datetime
from discord.utils import escape_markdown
from discord.ext import commands

from config import (
    EMOJIS_FOR_COGS, MAIN_COLOR, ORANGE_COLOR,
    EMOJIS, WEBSITE_LINK, SUPPORT_SERVER_LINK,
    INVITE_BOT_LINK, start_time
)
from utils.embed import error_embed
from utils.bot import EpicBot
from typing import Optional, Union


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
    async def userinfo(self, ctx: commands.Context, user: Optional[Union[discord.Member, discord.User]] = None):
        user = user or ctx.author

        embed = discord.Embed(color=user.color)
        embed.set_author(name=user, icon_url=user.display_avatar.url)
        embed.add_field(
            name="Basic Info",
            value=f"""
```yaml
Username: {user}
Nickname: {user.display_name}
ID: {user.id}
```
            """,
            inline=False
        )
        embed.add_field(
            name="Account Age Info",
            value=f"""
```yaml
Created At: {user.created_at.replace(tzinfo=None).strftime("%d/%m/%y | %H:%M:%S")}
Joined At: {"Not in server" if isinstance(user, discord.User) else user.joined_at.replace(tzinfo=None).strftime("%d/%m/%y | %H:%M:%S")}
```
            """,
            inline=False
        )

        roles = ""

        if isinstance(user, discord.Member):
            for role in user.roles[::-1]:
                if len(roles) > 500:
                    roles += "and more roles..."
                    break
                if str(role) != "@everyone":
                    roles += f"{role.mention}, "

            if len(roles) == 0:
                roles = "No roles."

            embed.add_field(
                name="Roles",
                value=roles,
                inline=False
            )

        embed.set_thumbnail(url=user.display_avatar.url)

        await ctx.reply(embed=embed)

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

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(aliases=['stats'], help="Get info about me!")
    async def botinfo(self, ctx):
        msg = await ctx.message.reply(embed=discord.Embed(title=f"Loading... {EMOJIS['loading']}"))
        embed = discord.Embed(
            title="Information About Me!",
            description="I am a simple, multipurpose Discord bot, built to make ur Discord life easier!",
            color=MAIN_COLOR
        ).set_thumbnail(url=self.client.user.display_avatar.url)
        embed.add_field(
            name="Stats",
            value=f"""
```yaml
Servers: {len(self.client.guilds)}
Users: {len(set(self.client.get_all_members()))}
Total Commands: {len(self.client.commands)}
Uptime: {str(datetime.timedelta(seconds=int(round(time.time()-start_time))))}
Version: V2 Rewrite
```
            """,
            inline=False
        )
#         async with self.client.session.get("https://statcord.com/logan/stats/751100444188737617") as r:
#             ah_yes = await r.json()
#         embed.add_field(
#             name="Statcord Stats",
#             value=f"""
# ```yaml
# Commands Ran Today: {ah_yes['data'][::-1][0]['commands']}
# Most Used Command: {ah_yes['data'][::-1][0]['popular'][0]['name']} - {ah_yes['data'][::-1][0]['popular'][0]['count']} uses
# Memory Usage: {'%.1f' % float(int(ah_yes['data'][::-1][0]['memactive'])/1000000000)} GB / {'%.1f' % float(int(psutil.virtual_memory().total)/1000000000)} GB
# Memory Load: {ah_yes['data'][::-1][0]['memload']}%
# CPU Load: {ah_yes['data'][::-1][0]['cpuload']}%
# ```
#             """,
#             inline=False
#         )
        embed.add_field(
            name="Links",
            value=f"""
- [Dashboard]({WEBSITE_LINK})
- [Support Server]({SUPPORT_SERVER_LINK})
- [Invite EpicBot]({INVITE_BOT_LINK})
- [Vote EpicBot]({WEBSITE_LINK}/vote)
            """,
            inline=True
        )
        embed.add_field(
            name="Owner Info",
            value="""
Made by: **[Nirlep\_5252\_](https://discord.com/users/558861606063308822)**
            """,
            inline=True
        )

        await msg.edit(embed=embed)


def setup(client):
    client.add_cog(info(client))

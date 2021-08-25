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
import time
import humanfriendly

from utils.embed import error_embed, success_embed
from discord.ext import commands
from config import EMOJIS, MAIN_COLOR, WEBSITE_LINK, SUPPORT_SERVER_LINK, CREDITS_CONTRIBUTORS, start_time, SUGGESTION_CHANNEL, BUG_REPORT_CHANNEL
from utils.bot import EpicBot


class misc(commands.Cog, description="Commands mostly related to the bot!"):
    def __init__(self, client: EpicBot):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(category="misc", help="Check bot's ping.")
    async def ping(self, ctx):
        time1 = time.perf_counter()
        msg = await ctx.message.reply(embed=discord.Embed(title=f"Pinging... {EMOJIS['loading']}", color=MAIN_COLOR))
        time2 = time.perf_counter()

        db_time1 = time.perf_counter()
        await self.client.prefixes.find_one({"_id": ctx.guild.id})
        db_time2 = time.perf_counter()

        shard_text = ""
        for shard, latency in self.client.latencies:
            shard_text += f"Shard {shard}" + ' ' * (3 - len(str(shard))) + f': {round(latency*1000)}ms\n'

        embed = success_embed(
            "🏓  Pong!",
            f"""
**Basic:**
```yaml
API      : {round(self.client.latency*1000)}ms
Bot      : {round((time2-time1)*1000)}ms
Database : {round((db_time2-db_time1)*1000)}ms
```
**Shards:**
```yaml
{shard_text}
```
            """
        ).set_thumbnail(url=self.client.user.display_avatar.url)
        await msg.edit(embed=embed)

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(category="misc", help="Invite EpicBot to your amazing server!")
    async def invite(self, ctx):
        await ctx.message.reply(embed=discord.Embed(
            title="Invite EpicBot \💖",
            description="Thank you so much!",
            color=MAIN_COLOR,
            url=f"https://discord.com/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot%20applications.commands"
        ).set_footer(text="UwU"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(category="misc", help="Vote EpicBot to gain perks!")
    async def vote(self, ctx):
        await ctx.message.reply(embed=discord.Embed(
            title="Vote EpicBot \💖",
            description="Thank you so much!",
            color=MAIN_COLOR,
            url=f"{WEBSITE_LINK}/vote"
        ).set_footer(text="I love you!"))

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(category="misc", aliases=['discord'], help="Join EpicBot's support server.")
    async def support(self, ctx):
        await ctx.message.reply(SUPPORT_SERVER_LINK)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(category="misc", help="Check EpicBot's uptime.")
    async def uptime(self, ctx):
        await ctx.message.reply(embed=discord.Embed(
            title="Uptime",
            description=f"I have been up for **{humanfriendly.format_timespan(round(time.time()-start_time))}**",
            color=MAIN_COLOR
        ))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(category="misc", help="Credits to our contributors and helpers!")
    async def credits(self, ctx):
        contributors = ""
        for e in CREDITS_CONTRIBUTORS:
            contributors += f"- [`{e}`](https://github.com/{CREDITS_CONTRIBUTORS[e][0]}) - {CREDITS_CONTRIBUTORS[e][1]}\n"
        await ctx.message.reply(embed=discord.Embed(
            title="Credits",
            description="This bot wouldn't have been possible without them!",
            color=MAIN_COLOR
        ).set_thumbnail(url=self.client.user.display_avatar.url).add_field(
            name="Owner",
            value="- [`Nirlep_5252_`](https://github.com/Nirlep5252)",
            inline=False
        ).add_field(
            name="Contributors",
            value=contributors,
            inline=False
        ).add_field(
            name="Other Credits",
            value="""
- [`Tech-Struck`](https://github.com/TechStruck/TechStruck-Bot) - Run command
- [`Hexbot`](https://github.com/1Prototype1/HexBot) - Game commands
            """,
            inline=False
        ).set_footer(text="They are amazing 💖"))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(category="misc", help="View our privacy policy")
    async def privacy(self, ctx):
        await ctx.message.reply(f"You can view our privacy policy here {WEBSITE_LINK}/privacy")

    @commands.cooldown(3, 120, commands.BucketType.user)
    @commands.command(category="misc", help="Submit a suggestion!")
    async def suggest(self, ctx, *, suggestion=None):
        prefix = ctx.clean_prefix

        if suggestion is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Incorrect Usage!",
                f"Please use it like this: `{prefix}suggest <suggestion>`"
            ))

        user_profile = await self.client.get_user_profile_(ctx.author.id)
        user_profile.update({"suggestions_submitted": user_profile['suggestions_submitted'] + 1})

        files = []
        for file in ctx.message.attachments:
            files.append(await file.to_file())

        embed = success_embed("Suggestion!", suggestion
                ).set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url
                ).set_footer(text=f"User ID: {ctx.author.id} | Guild ID: {ctx.guild.id}")

        msg = await self.client.get_channel(SUGGESTION_CHANNEL).send(embed=embed, files=files)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await ctx.reply(embed=success_embed(
            f"{EMOJIS['tick_yes']} Suggestion submitted!",
            f"Thank you for submitting the suggestion!\nYou have suggested a total of `{user_profile['suggestions_submitted']}` suggestions!"
        ))

    @commands.cooldown(2, 7200, commands.BucketType.user)
    @commands.command(category="misc", aliases=['bug'], help="Report a buggie >~<")
    async def bugreport(self, ctx, *, bug=None):
        prefix = ctx.clean_prefix
        if bug is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed("Incorrect Usage", f"Please use it like this: `{prefix}bug <bug>`"))
        user_profile = await self.client.get_user_profile_(ctx.author.id)
        user_profile.update({"bugs_reported": user_profile['bugs_reported'] + 1})
        embed = discord.Embed(
            title="Bug",
            description=f"""
```
{bug}
```
            """,
            color=MAIN_COLOR
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
        embed.set_footer(text=f"User ID: {ctx.author.id} | Guild ID: {ctx.guild.id}")
        await self.client.get_channel(BUG_REPORT_CHANNEL).send(embed=embed)
        await ctx.reply(embed=success_embed(
            f"{EMOJIS['tick_yes']} Bug submitted!",
            f"Thank you for submitting the bug!\nYou have reported a total of `{user_profile['bugs_reported']}` bugs"
        ))


def setup(client):
    client.add_cog(misc(client))

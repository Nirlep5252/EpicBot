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

from discord.ext import commands
from utils.embed import success_embed, error_embed
from discord.utils import escape_markdown
from utils.custom_checks import bot_mods_only
from utils.bot import EpicBot
from config import (
    EMOJIS, DB_UPDATE_INTERVAL, OWNERS
)


class Devsonly(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client

    @commands.is_owner()
    @commands.command(help="Load jsk!")
    async def loadjsk(self, ctx):
        msg = await ctx.reply(f"{EMOJIS['loading']} Working on it...")
        self.client.load_extension('jishaku')
        await msg.edit(content="Done!")

    @commands.is_owner()
    @commands.command(aliases=['getcache'], help="Get cache!")
    async def get_cache(self, ctx: commands.Context):
        msg = await ctx.reply(f"{EMOJIS['loading']} Working on it...")
        await self.client.get_cache()
        await msg.edit(content="Done!")

    @commands.is_owner()
    @commands.command(aliases=['updatedb'], help="Update the database!")
    async def update_db(self, ctx: commands.Context, db=None):
        if db is None:
            return await ctx.reply("""
Please select a database next time:

- prefixes
- serverconfig
            """)
        msg = await ctx.reply(f"{EMOJIS['loading']} Updating...")
        if db.lower() in ['prefixes', 'prefix']:
            await self.client.update_prefixes_db()
        if db.lower() in ['server', 'serverconfig']:
            await self.client.update_serverconfig_db()
        return await msg.edit(content="Updated!")

    @bot_mods_only()
    @commands.command(help="Check when the database was last updated.")
    async def lastdb(self, ctx: commands.Context):
        await ctx.reply(embed=success_embed(
            f"{EMOJIS['tick_yes']} Database info!",
            f"""
```yaml
Prefix DB: {round(time.time() - self.client.last_updated_prefixes_db)} seconds ago
Serverconfig DB: {round(time.time() - self.client.last_updated_serverconfig_db)} seconds ago
Leveling DB: {round(time.time() - self.client.last_updated_leveling_db)} seconds ago
User profile DB: {round(time.time() - self.client.last_updated_user_profile_db)} seconds ago
```
            """
        ).set_footer(text=f"Database is updated every {DB_UPDATE_INTERVAL} seconds."))

    @bot_mods_only()
    @commands.command(help="Blacklist some kid.")
    @commands.cooldown(3, 120, commands.BucketType.user)
    async def blacklist(self, ctx: commands.Context, user: discord.User = None, *, reason='No Reason Provided'):
        prefix = ctx.clean_prefix
        if user is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Mention who you wanna blacklist next time.\nExample: `{prefix}blacklist @egirl spamming`"
            ))
        if user == ctx.author or user.id in OWNERS:
            return await ctx.reply("no")
        for e in self.client.blacklisted_cache:
            if e['_id'] == user.id:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Error!",
                    f"This kid is already blacklisted.\n```yaml\nReason: {e['reason']}\n```"
                ))
        await self.client.blacklisted.insert_one({
            "_id": user.id,
            "reason": reason
        })
        await self.client.get_blacklisted_users()
        return await ctx.reply(embed=success_embed(
            f"{EMOJIS['tick_yes']} Kid Blacklisted!",
            f"Done! I have blacklisted **{escape_markdown(str(user))}**."
        ))

    @bot_mods_only()
    @commands.command(help="Unblacklist some kid.")
    @commands.cooldown(3, 120, commands.BucketType.user)
    async def unblacklist(self, ctx: commands.Context, user: discord.User = None):
        prefix = ctx.clean_prefix
        if user is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Mention who you wanna unblacklist next time.\nExample: `{prefix}unblacklist @egirl`"
            ))
        for e in self.client.blacklisted_cache:
            if e['_id'] == user.id:
                await self.client.blacklisted.delete_one({
                    "_id": user.id
                })
                await self.client.get_blacklisted_users()
                return await ctx.message.reply(embed=success_embed(
                    f"{EMOJIS['tick_yes']} Kid Unblacklisted!",
                    f"Done! I have unblacklisted **{escape_markdown(str(user))}**.\n```yaml\nReason: {e['reason']}\n```"
                ))
        ctx.command.reset_cooldown(ctx)
        return await ctx.message.reply(embed=error_embed(
            f"{EMOJIS['tick_yes']} Kid Not Found!",
            f"Looks like **{escape_markdown(str(user))}** is not blacklisted, please try again."
        ))

    @commands.is_owner()
    @commands.command(help="DM some kid.")
    async def dm(self, ctx: commands.Context, user_id: int = None, *, msg=None):
        prefix = ctx.clean_prefix
        if user_id is None:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Mention who you wanna unblacklist next time.\nExample: `{prefix}dm 679677267164921866 UwU Hi Cutie!`"
            ))
        if msg is None:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter a message next time.\nExample: `{prefix}dm 679677267164921866 UwU Hi Cutie!`"
            ))
        user = self.client.get_user(user_id)
        if user is None:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid User!",
                "Looks like that user doesn't exist, please try again."
            ))
        await user.send(msg)
        await ctx.reply(f"{EMOJIS['tick_yes']} Successfully DMed **{escape_markdown(str(user))} ({user_id})**")


def setup(client):
    client.add_cog(Devsonly(client))

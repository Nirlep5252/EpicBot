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
import traceback

from utils.embed import success_embed
from discord.ext import commands, tasks
from config import ERROR_LOG_CHANNEL
from utils.bot import EpicBot


class BumpReminder(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client
        self.auth_str = "bump done"
        self.disboard_id = 302050872383242240
        self.error_channel = self.client.get_channel(ERROR_LOG_CHANNEL)
        self.peng = discord.AllowedMentions(
            everyone=False,
            roles=True,
            users=True,
            replied_user=False
        )
        self.bumploop.start()

    @commands.Cog.listener("on_message")
    async def on_bump_message(self, message):
        if message.author.id != self.disboard_id or len(message.embeds) == 0:
            return
        if self.auth_str not in str(message.embeds[0].description).lower():
            return
        g = await self.client.get_guild_config(message.guild.id)
        if not g['bump_reminders']:
            return
        next_bump_time = time.time() + 60 * 60 * 2

        bumper = None
        async for msg in message.channel.history(limit=3):
            if msg.content.lower().startswith("!d bump"):
                bumper = msg.author.id

        g['bump_reminders'].update({
            'channel_id': message.channel.id,
            'time': next_bump_time,
            'bumper': message.author.id if bumper is None else bumper
        })
        await message.add_reaction("⏱️")

    @tasks.loop(seconds=30)
    async def bumploop(self):
        await self.client.wait_until_ready()
        try:
            time_now = time.time()
            for e in self.client.serverconfig_cache:
                if e['bump_reminders']:
                    e = e['bump_reminders']

                    if e['time'] is not None:
                        if round(e['time']) <= round(time_now):
                            await self.client.get_channel(e['channel_id']).send(
                                f"<@&{e['role']}>" if e['role'] is not None else f"<@{e['bumper']}>",
                                embed=success_embed("It's Bump Time", "Please bump using `!d bump`."),
                                allowed_mentions=self.peng
                            )
                            e.update({"time": None})
        except Exception:
            cancer_error = traceback.format_exc()
            await self.error_channel.send(f"ERROR IN BUMP LOOP ```py\n{cancer_error}\n```")


def setup(client):
    client.add_cog(BumpReminder(client))

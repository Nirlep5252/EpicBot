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
from discord.ext import commands
from utils.bot import EpicBot
from config import ANTIHOIST_CHARS


class Antihoist(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if after.bot:
            return
        g = await self.client.get_guild_config(after.guild.id)
        if not g['antihoisting']:
            return

        if after.display_name[0] in ANTIHOIST_CHARS and not after.display_name.startswith("[AFK] "):
            try:
                await after.edit(
                    nick=before.display_name if before.display_name[0] not in ANTIHOIST_CHARS else "Moderated Nickname",
                    reason="EpicBot Antihoisting"
                )
            except Exception:
                pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return
        g = await self.client.get_guild_config(member.guild.id)
        if not g['antihoisting']:
            return

        if member.display_name[0] in ANTIHOIST_CHARS:
            try:
                await member.edit(
                    nick="Moderated Nickname",
                    reason="EpicBot Antihoisting"
                )
            except Exception:
                pass


def setup(client):
    client.add_cog(Antihoist(client))

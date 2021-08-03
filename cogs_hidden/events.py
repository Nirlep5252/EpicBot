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


class Events(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client

    @commands.Cog.listener("on_thread_join")
    async def ticket_roles_mention(self, thread: discord.Thread):
        if not thread.name.startswith("ticket-"):
            return
        try:
            int(thread.name[7:])
        except Exception:
            return
        g = await self.client.get_guild_config(thread.guild.id)
        if not g['tickets']['channel']:
            return
        if not g['tickets']['message_id']:
            return
        if thread.parent_id != g['tickets']['channel']:
            return
        if len(g['tickets']['roles']) == 0:
            return
        role_text = ""
        for role in g['tickets']['roles']:
            role_text += f"<@&{role}> "
        await thread.send(role_text, allowed_mentions=discord.AllowedMentions(
            roles=True,
            everyone=False,
            users=False,
            replied_user=False
        ))


def setup(client: EpicBot):
    client.add_cog(Events(client))

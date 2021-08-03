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


class Counting(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client

    @commands.Cog.listener("on_message")
    async def count_go_brr(self, message: discord.Message):
        if message.author.bot:
            return
        g = await self.client.get_guild_config(message.guild.id)
        if not g['counting']:
            return
        if message.channel.id != g['counting']['channel']:
            return
        try:
            number = int(message.content)
        except Exception:
            return await message.delete()

        if message.author.id == g['counting']['last_user']:
            return await message.delete()
        if number != g['counting']['count'] + 1:
            return await message.delete()

        g['counting'].update({
            "count": number,
            "last_user": message.author.id,
            "count_msg": message.id
        })
        await message.add_reaction('✅')

    @commands.Cog.listener("on_message_delete")
    async def listen_here_you_little_shit(self, message: discord.Message):
        if message.author.bot:
            return
        g = await self.client.get_guild_config(message.guild.id)
        if not g['counting']:
            return
        if message.channel.id != g['counting']['channel']:
            return
        if message.id != g['counting']['count_msg']:
            return

        await message.channel.send(f"`{message.author}` deleted their count, the current count is: `{g['counting']['count']}`")


def setup(client):
    client.add_cog(Counting(client))

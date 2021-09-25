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
import random

from discord.ext import commands
from config import CUTE_EMOJIS
from utils.bot import EpicBot


class VoteTracking(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client
        self.vote_tracking_bot_id = 891172840181743697
        self.vote_scraping_channel_id = 851658500118413313
        self.vote_sending_channel_id = 776015595354325002

    @commands.Cog.listener("on_message")
    async def haha_vot_go_brr(self, message: discord.Message):
        if message.author.id != self.vote_tracking_bot_id:
            return
        if message.channel.id != self.vote_scraping_channel_id:
            return
        if len(message.embeds) != 1:
            return
        embed = message.embeds[0]
        desc = embed.description
        try:
            voter_id = int(desc[2:20])
            votes = "<work in progress>"
            channel = self.client.get_channel(self.vote_sending_channel_id)
            await channel.send(
                f"Thank you <@{voter_id}> for voting me! UwU~ {random.choice(CUTE_EMOJIS)}\nYou have a total of **{votes}** votes now! {random.choice(CUTE_EMOJIS)}",
                allowed_mentions=discord.AllowedMentions(
                    users=True,
                    everyone=False,
                    roles=False,
                    replied_user=False
                )
            )
        except Exception:
            return


def setup(client):
    client.add_cog(VoteTracking(client))

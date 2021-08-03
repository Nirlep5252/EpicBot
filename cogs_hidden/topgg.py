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

import dbl

from discord.ext import commands
from config import TOP_GG_TOKEN, EMOJIS
from utils.bot import EpicBot


class TopGG(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client
        self.token = TOP_GG_TOKEN
        self.vote_c_id = 776015595354325002
        self.dblpy = dbl.DBLClient(
            self.client,
            self.token,
            webhook_path='/sus',
            webhook_auth='amogus',
            webhook_port=8080
        )

    # this does not work
    # shocker
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        user = self.client.get_user(data['user'])
        channel = self.client.get_channel(self.vote_c_id)
        await channel.send(f"Thank you {user.mention} for voting! {EMOJIS['heawt']}")

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        test_user = self.client.get_user(data['user'])
        channel = self.clent.get_channel(self.vote_c_id)
        await channel.send(f"webhooks works lmfao {test_user.mention}")


def setup(client):
    client.add_cog(TopGG(client))

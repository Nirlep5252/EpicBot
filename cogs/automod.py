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

class AutomodConfigView(discord.ui.View):
    def __init__(self, ctx: commands.Context, embeds: list):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.embeds = embeds


    @discord.ui.button(label = "Filters Config", style=discord.ButtonStyle.blurple)
    async def filter_show(self, b: discord.Button, i: discord.Interaction):
        for item in self.children:
            item.disabled = False
        b.disabled = True
        await i.message.edit(embed=self.embeds[0], view=self)

    @discord.ui.button(label="Whitelist Config", style=discord.ButtonStyle.green)
    async def whitelist_show(self, b: discord.Button, i: discord.Interaction):
        for item in self.children:
            item.disabled = False
        b.disabled = True
        await i.message.edit(embed=self.embeds[1], view=self)

    async def interaction_check(self, i: discord.Interaction):
        if i.user != self.ctx.author:
            return await i.response.send_message("You cannot interaction in other's command!", ephemeral=True)
        return True



class automod(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client


def setup(client: EpicBot):
    client.add_cog(automod(client))

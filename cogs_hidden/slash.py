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

# import discord
from discord.ext import commands
from utils.bot import EpicBot
# from utils.embed import success_embed
# from random import randint


class LolSlashCmdGoBrr(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client

    # @commands.Cog.listener("on_interaction")
    # async def haha_slash_go_brr(self, interaction: discord.Interaction):
    #     if interaction.type == discord.InteractionType.application_command:
    #         await interaction.response.send_message(
    #             embed=success_embed(
    #                 title="<:amogus:871732356233429014>  Sussometer",
    #                 description=f"You are **{randint(0, 100)}%** sus!"
    #             )
    #         )


def setup(client: EpicBot):
    client.add_cog(LolSlashCmdGoBrr(client))

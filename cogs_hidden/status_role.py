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

from discord.ext import commands
from utils.bot import EpicBot

PERKS = """
**Here are your perks! Hope you enjoy! :D**

`-` Image and embed perms in <#746202728375648273>
`-` Access to special autoposting channels.
`-` Dyno bypass! (can post links)
`-` Special hoisted role above other members :3

**Thank you cutie!~ <3**
"""


class StatusRole(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client
        self.status = ".gg/nirlep"

    @commands.Cog.listener("on_presence_update")
    async def sex(self, before, after):

        if before.bot:
            return
        guild = self.client.get_guild(746202728031584358)
        if before.guild.id != guild.id:
            return

        if before.activity == after.activity:
            return

        role = guild.get_role(853174979758522388)

        if self.status in str(after.activity).lower() and role not in after.roles:
            await after.add_roles(role, reason="Thank you for having 'discord.gg/nirlep' in your status!")
            # await after.send(embed=success_embed(
            #     f"<a:hugs:839739273083224104>  I love you!",
            #     f"**Thank you for having `discord.gg/nirlep` in your status!**\n{PERKS}"
            # ).set_thumbnail(url="https://cdn.discordapp.com/emojis/802801495153967154.png?v=1"))

        elif self.status not in str(after.activity).lower() and role in after.roles:
            await after.remove_roles(role, reason="Pain. This kid removed 'discord.gg/nirlep' from their status.")


def setup(client):
    client.add_cog(StatusRole(client))

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

from logging import basicConfig, INFO
from config import BOT_TOKEN
from utils.bot import EpicBot
from os import environ

basicConfig(level=INFO)

client = EpicBot()
environ.setdefault("JISHAKU_HIDE", "1")
environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")


@client.check
async def check_commands(ctx):
    if ctx.guild is None:
        return False
    g = await client.get_guild_config(ctx.guild.id)
    dc = g['disabled_cmds']
    dch = g['disabled_channels']
    return (ctx.guild is not None) and (ctx.command.name not in dc) and (ctx.channel.id not in dch)


if __name__ == '__main__':
    client.run(BOT_TOKEN)

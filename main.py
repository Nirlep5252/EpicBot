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
from discord import (
    Intents,
    AllowedMentions,
    Activity,
    ActivityType
)
from config import EMOJIS, BOT_TOKEN
from utils.embed import success_embed
from utils.bot import EpicBot
from utils.help import EpicBotHelp
from os import environ
from utils.ui import TicketView

basicConfig(level=INFO)

intents = Intents.default()
intents.members = True
client = EpicBot(
    command_prefix=EpicBot.get_custom_prefix,
    intents=Intents.all(),
    case_insensitive=True,
    allowed_mentions=AllowedMentions.none(),
    strip_after_prefix=True,
    help_command=EpicBotHelp(),
    cached_messages=10000
)
environ.setdefault("JISHAKU_HIDE", "1")
environ.setdefault("JISHAKU_NO_UNDERSCORE", "1")


@client.check
async def check_commands(ctx):
    if ctx.guild is not None:
        g = await client.get_guild_config(ctx.guild.id)
        dc = g['disabled_cmds']
        dch = g['disabled_channels']
    return (ctx.guild is not None) and (ctx.command.name not in dc) and (ctx.channel.id not in dch)


@client.event
async def on_message(message):
    if not client.cache_loaded:
        return
    if message.author.bot:
        return
    for e in client.blacklisted_cache:
        if message.author.id == e['_id']:
            return
    if message.content.lower() in [f'<@{client.user.id}>', f'<@!{client.user.id}>']:
        prefixes = await client.fetch_prefix(message)
        prefix_text = ""
        for prefix in prefixes:
            prefix_text += f"`{prefix}`, "
        prefix_text = prefix_text[:-2]
        return await message.reply(embed=success_embed(
            f"{EMOJIS['wave_1']} Hello!",
            f"My prefix{'es' if len(prefixes) > 1 else ''} for this server {'are' if len(prefixes) > 1 else 'is'}: {prefix_text}"
        ))

    await client.process_commands(message)


@client.event
async def on_message_edit(before, after):
    if before.content == after.content:
        return
    if before.author.bot:
        return
    client.dispatch("message", after)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(activity=Activity(
        type=ActivityType.playing,
        name="e/help | beta.epic-bot.com"
    ))

    client.add_view(TicketView())

    client.load_extension('jishaku')
    print("Loaded jsk!")

    await client.get_cache()
    await client.get_blacklisted_users()
    client.cache_loaded = True

    await client.load_extensions('./cogs')
    await client.load_extensions('./cogs_hidden')
    client.load_extension('how_slash')

if __name__ == '__main__':
    client.run(BOT_TOKEN)

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
from utils.help2 import EpicBotHelp
from os import environ
from utils.ui import ButtonSelfRoleView, DropDownSelfRoleView, TicketView

basicConfig(level=INFO)

intents = Intents.default()
intents.members = True
client = EpicBot(
    command_prefix=EpicBot.get_custom_prefix,
    intents=intents,
    case_insensitive=True,
    allowed_mentions=AllowedMentions.none(),
    strip_after_prefix=True,
    help_command=EpicBotHelp(),
    cached_messages=10000,
    activity=Activity(type=ActivityType.playing, name="e!help | epic-bot.com")
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
    if not client.cache_loaded:
        return
    if not client.cogs_loaded:
        return
    client.dispatch("message", after)

if not client.cache_loaded:
    client.loop.run_until_complete(client.get_cache())
    client.loop.run_until_complete(client.get_blacklisted_users())
    client.cache_loaded = True

if not client.cogs_loaded:
    client.load_extension('jishaku')
    print("Loaded jsk!")
    client.loop.run_until_complete(client.load_extensions('./cogs'))
    client.loop.run_until_complete(client.load_extensions('./cogs_hidden'))
    client.cogs_loaded = True


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    if not client.views_loaded:
        client.add_view(TicketView())
        client.views_loaded = True
        print("Ticket view has been loaded.")

    if not client.rolemenus_loaded:
        i = 0
        cursor = client.self_roles.find({})
        h = await cursor.to_list(length=None)
        for amogus in h:
            guild = client.get_guild(amogus['_id'])
            if guild is not None:
                role_menus = amogus['role_menus']
                for msg_id, menu in role_menus.items():
                    if menu['type'] == 'dropdown':
                        client.add_view(DropDownSelfRoleView(guild, menu['stuff']), message_id=int(msg_id))
                        i += 1
                    if menu['type'] == 'button':
                        client.add_view(ButtonSelfRoleView(guild, menu['stuff']), message_id=int(msg_id))
                        i += 1
        client.rolemenus_loaded = True

        print(f"{i} Self role views has been loaded.")

if __name__ == '__main__':
    client.run(BOT_TOKEN)

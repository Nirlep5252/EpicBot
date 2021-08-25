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
import urllib
import re
import emojis
from discord.ext import commands
from config import (
    DEFAULT_BANNED_WORDS, GLOBAL_CHAT_RULES,
    EMOJIS, RED_COLOR, EMPTY_CHARACTER, OWNERS
)
from utils.embed import success_embed, error_embed
from collections import Counter
from utils.ui import Confirm
from utils.bot import EpicBot


class GlobalChat(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client
        self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        self.invite_regex = re.compile(r'((http(s|):\/\/|)(discord)(\.(gg|io|me)\/|app\.com\/invite\/)([0-z]+))')
        self.zalgo_regex = re.compile(r"%CC%", re.MULTILINE)

        self.cooldown = commands.CooldownMapping.from_cooldown(1, 2, commands.BucketType.user)
        self.peng = discord.AllowedMentions.none()

        self.confirmation_cooldown = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user)

        self.replace_stuff = [
            '\n', ' ', '~', '.', ',', '!', EMPTY_CHARACTER,
            '*', '@', '#', '$', '%', '^', '&', '(', ')', '-',
            '_', '=', '+', '/', '\\', ';', ':', '[', ']', '{',
            '}', '\'', '"', '<', '>', '?', '`', '|', '\t', '\r',
            '​'
        ]

    def isinglish(self, s: str):
        s = emojis.decode(s)
        try:
            s.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True

    async def check_message(self, content: str, user_id: int) -> bool:
        temp_cont = content

        for stuff in self.replace_stuff:
            temp_cont = temp_cont.replace(stuff, "")

        for w in DEFAULT_BANNED_WORDS:
            if w in temp_cont.lower():
                return False

        if not self.isinglish(content):
            return False

        if len(content) > 150:
            c_ = Counter(content.lower())
            for c, n in c_.most_common(None):
                if c != ' ' and len(content) / n < 8:
                    return False

        if len(content) > 500:
            return False

        invite_match = self.invite_regex.findall(content)
        if invite_match:
            return False

        if re.search(self.url_regex, content) and user_id not in OWNERS:
            return False

        if self.zalgo_regex.search(urllib.parse.quote(content.encode("utf-8"))):
            return False

        return True

    @commands.Cog.listener("on_message")
    async def global_chat(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        bucket = self.cooldown.get_bucket(message)
        retry_after = bucket.update_rate_limit()

        if retry_after and message.author.id != 558861606063308822:
            return

        g = await self.client.get_guild_config(message.guild.id)
        p = await self.client.get_user_profile_(message.author.id)
        if not g['globalchat']:
            return
        if message.channel != self.client.get_channel(g['globalchat']):
            return

        if not await self.check_message(message.content, message.author.id) or message.content == "":
            await message.add_reaction('❌')
            return

        for e in self.client.blacklisted_cache:
            if message.author.id == e['_id']:
                return

        if message.edited_at is not None:
            return

        if not p['gc_rules_accepted']:
            await message.add_reaction('❌')
            bucket_ = self.confirmation_cooldown.get_bucket(message)
            retry_after_ = bucket_.update_rate_limit()
            if retry_after_:
                return
            ctx = await self.client.get_context(message)
            v = Confirm(context=ctx)
            msg__ = await message.author.send(
                "Hey, looks like it is your first time sending a message in global chat!\nPlease read and accept these rules to continue sending messages in global chat.",
                embed=success_embed("🌍 Global chat rules", GLOBAL_CHAT_RULES),
                view=v
            )
            await v.wait()
            if v.value is None:
                return await msg__.edit(content="", embed=error_embed("Too late.", "You didn't respond in time."), view=None)
            if not v.value:
                return await msg__.edit(content="", embed=discord.Embed(title=f"{EMOJIS['tick_no']} Cancelled.", color=RED_COLOR), view=None)
            p.update({"gc_rules_accepted": True})
            return await msg__.edit(content="", embed=success_embed("Thank you.", "Enjoy chatting with people :D"), view=None)

        for g in self.client.serverconfig_cache:
            if g['globalchat']:
                channel = self.client.get_channel(g['globalchat'])
                if channel and channel != message.channel:
                    webhooks = await channel.webhooks()
                    webhook = discord.utils.get(webhooks, name="EpicBot Global Chat", user=self.client.user)
                    if webhook is None:
                        webhook = await channel.create_webhook(name="EpicBot Global Chat")

                    await webhook.send(
                        message.content,
                        allowed_mentions=self.peng,
                        username=str(message.author) if p['gc_nick'] is None or channel.id == 863375202284077066 else p['gc_nick'],
                        avatar_url=message.author.display_avatar.url if p['gc_avatar'] is None or channel.id == 863375202284077066 else p['gc_avatar']
                    )


def setup(client):
    client.add_cog(GlobalChat(client))

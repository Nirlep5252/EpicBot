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
import re
import urllib

from discord.ext import commands
from config import DEFAULT_BANNED_WORDS, EMOJIS, RED_COLOR
from datetime import datetime
from re import search
from collections import Counter
from utils.bot import EpicBot


class Automod(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client
        self.peng = discord.AllowedMentions(
            everyone=False,
            roles=False,
            users=True,
            replied_user=False
        )
        self.url_regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        self.invite_regex = re.compile(r'((http(s|):\/\/|)(discord)(\.(gg|io|me)\/|app\.com\/invite\/)([0-z]+))')
        self.zalgo_regex = re.compile(r"%CC%", re.MULTILINE)

    async def is_enabled(self, guild_id, module):
        g = await self.client.get_guild_config(guild_id)
        am = g['automod']

        if not am[module]['enabled']:
            return False

        return [am[module], g]

    def mod_perms(self, m):
        p = m.author.guild_permissions

        if p.kick_members or p.administrator or p.ban_members or p.manage_guild or m.author == m.guild.owner:
            return True
        else:
            return False

    @commands.Cog.listener("on_message")
    async def bad_word_automod(self, msg):
        if msg.author.bot or msg.content == "" or not msg.guild:
            return

        m_ = await self.is_enabled(msg.guild.id, "banned_words")
        if not m_:
            return

        m = m_[0]
        g = m_[1]

        if self.mod_perms(msg):
            return

        if msg.channel.id in g['automod']['ignored_channels']:
            return

        for r in msg.author.roles:
            if r.id in g['automod']['allowed_roles']:
                return

        for w in DEFAULT_BANNED_WORDS:
            if w in msg.content.lower():
                await msg.delete()
                return await msg.channel.send(
                    f"{msg.author.mention}, Watch your language.",
                    delete_after=5,
                    allowed_mentions=self.peng
                )

        for w in m['words']:
            if w in msg.content.lower():
                await msg.delete()
                return await msg.channel.send(
                    f"{msg.author.mention}, Watch your language.",
                    delete_after=5,
                    allowed_mentions=self.peng
                )

    @commands.Cog.listener("on_message")
    async def all_caps(self, msg):
        if msg.author.bot or msg.content == "" or not msg.guild or len(msg.content) < 5:
            return
        m_ = await self.is_enabled(msg.guild.id, "all_caps")
        if not m_:
            return
        g = m_[1]

        if self.mod_perms(msg):
            return

        if msg.channel.id in g['automod']['ignored_channels']:
            return

        for r in msg.author.roles:
            if r.id in g['automod']['allowed_roles']:
                return

        if msg.content.isupper():
            await msg.delete()
            return await msg.channel.send(
                f"{msg.author.mention}, Too many caps.",
                delete_after=5,
                allowed_mentions=self.peng
            )

        upper_count = 0
        lower_count = 0

        for h in msg.content:
            if h.isupper():
                upper_count += 1
            else:
                lower_count += 1

        if (upper_count / len(msg.content)) * 100 > 70:
            await msg.delete()
            return await msg.channel.send(
                f"{msg.author.mention}, Too many caps.",
                delete_after=5,
                allowed_mentions=self.peng
            )

    @commands.Cog.listener("on_message")
    async def duplicate_text(self, msg):
        if msg.author.bot or not msg.guild or len(msg.content) < 100:
            return
        m_ = await self.is_enabled(msg.guild.id, "duplicate_text")
        if not m_:
            return
        g = m_[1]
        if self.mod_perms(msg):
            return
        if msg.channel.id in g['automod']['ignored_channels']:
            return
        for r in msg.author.roles:
            if r.id in g['automod']['allowed_roles']:
                return

        c_ = Counter(msg.content.lower())
        for c, n in c_.most_common(None):
            if c != ' ' and len(msg.content) / n < 9:
                await msg.delete()
                return await msg.channel.send(
                    f"{msg.author.mention}, No spamming.",
                    delete_after=5,
                    allowed_mentions=self.peng
                )

    @commands.Cog.listener("on_message")
    async def fast_msg_spam(self, msg):
        def _check(m):
            return (m.author == msg.author and (datetime.utcnow() - m.created_at.replace(tzinfo=None)).seconds < 7)
        if msg.author.bot or not msg.guild:
            return
        m_ = await self.is_enabled(msg.guild.id, "message_spam")
        if not m_:
            return
        g = m_[1]
        if self.mod_perms(msg):
            return
        if msg.channel.id in g['automod']['ignored_channels']:
            return
        for r in msg.author.roles:
            if r.id in g['automod']['allowed_roles']:
                return

        h = list(filter(lambda m: _check(m), self.client.cached_messages))

        if len(h) >= 5:
            await msg.channel.purge(limit=5, check=_check)
            return await msg.channel.send(
                f"{msg.author.mention}, Stop spamming.",
                delete_after=5,
                allowed_mentions=self.peng
            )

    @commands.Cog.listener("on_message")
    async def discord_invites(self, msg):
        if msg.author.bot or not msg.guild:
            return
        m_ = await self.is_enabled(msg.guild.id, 'invites')
        if not m_:
            return
        g = m_[1]
        if self.mod_perms(msg):
            return
        if msg.channel.id in g['automod']['ignored_channels']:
            return
        for r in msg.author.roles:
            if r.id in g['automod']['allowed_roles']:
                return

        invite_match = self.invite_regex.findall(msg.content)
        if invite_match:
            for e in invite_match:
                try:
                    invite = await self.client.fetch_invite(e[-1])
                except discord.NotFound:
                    pass
                else:
                    if not invite.guild.id == msg.guild.id:
                        await msg.delete()
                        return await msg.channel.send(
                            f"{msg.author.mention}, No invite links.",
                            delete_after=5,
                            allowed_mentions=self.peng
                        )

    @commands.Cog.listener("on_message")
    async def links(self, msg):
        if msg.author.bot or not msg.guild:
            return
        m_ = await self.is_enabled(msg.guild.id, "links")
        if not m_:
            return
        g = m_[1]
        if self.mod_perms(msg):
            return
        if msg.channel.id in g['automod']['ignored_channels']:
            return
        for r in msg.author.roles:
            if r.id in g['automod']['allowed_roles']:
                return

        if search(self.url_regex, msg.content):
            await msg.delete()
            return await msg.channel.send(
                f"{msg.author.mention}, No links allowed.",
                delete_after=5,
                allowed_mentions=self.peng
            )

    @commands.Cog.listener("on_message")
    async def mass_mentions(self, msg):
        if msg.author.bot or not msg.guild:
            return
        m_ = await self.is_enabled(msg.guild.id, "mass_mentions")
        if not m_:
            return
        g = m_[1]
        if self.mod_perms(msg):
            return
        if msg.channel.id in g['automod']['ignored_channels']:
            return
        for r in msg.author.roles:
            if r.id in g['automod']['allowed_roles']:
                return

        if len(msg.mentions) >= 3:
            await msg.delete()
            return await msg.channel.send(
                f"{msg.author.mention}, Don't spam mentions.",
                delete_after=5,
                allowed_mentions=self.peng
            )

    @commands.Cog.listener("on_message")
    async def emoji_spam(self, msg):
        if msg.author.bot or not msg.guild:
            return
        m_ = await self.is_enabled(msg.guild.id, "emoji_spam")
        if not m_:
            return
        g = m_[1]
        if self.mod_perms(msg):
            return
        if msg.channel.id in g['automod']['ignored_channels']:
            return
        for r in msg.author.roles:
            if r.id in g['automod']['allowed_roles']:
                return

    @commands.Cog.listener("on_message")
    async def zalgo_text(self, msg):
        if msg.author.bot or not msg.guild:
            return
        m_ = await self.is_enabled(msg.guild.id, "zalgo_text")
        if not m_:
            return
        g = m_[1]
        if self.mod_perms(msg):
            return
        if msg.channel.id in g['automod']['ignored_channels']:
            return
        for r in msg.author.roles:
            if r.id in g['automod']['allowed_roles']:
                return

        x = self.zalgo_regex.search(urllib.parse.quote(msg.content.encode("utf-8")))
        if x:
            await msg.delete()
            return await msg.channel.send(
                f"{msg.author.mention}, No zalgo allowed.",
                delete_after=5,
                allowed_mentions=self.peng
            )

    @commands.Cog.listener("on_message_delete")
    async def ghostping_delete(self, msgobj):

        if len(msgobj.mentions) == 0 or msgobj.author.bot:
            return

        g = await self.client.get_guild_config(msgobj.guild.id)
        if not g['ghost_ping']:
            return

        time_created = int(msgobj.created_at.strftime("%H%M%S"))
        time_now = int(datetime.utcnow().strftime("%H%M%S"))
        delta = time_now - time_created

        if delta > 11:
            return

        mentions = msgobj.role_mentions
        for i in msgobj.mentions:
            if not i.bot:
                if not i == msgobj.author:
                    mentions.append(i)

        if mentions or msgobj.mention_everyone:
            string = ""
            for i in mentions:
                string += f" {i.mention}"
            if msgobj.mention_everyone:
                string += " (@everyone / @here)"
            E = discord.Embed(
                title=f"{EMOJIS['hu_peng']} Ghost ping detected!",
                # description=f"**Victims** : {string}\n**Message:** {msgobj.content}",
                timestamp=msgobj.created_at,
                color=RED_COLOR
            ).set_author(name=msgobj.author, icon_url=msgobj.author.display_avatar.url
            ).add_field(name="Offender:", value=msgobj.author.mention, inline=False
            ).add_field(name="Victims:", value=string, inline=False
            ).set_thumbnail(url="https://cdn.discordapp.com/emojis/527884882010177536.png?v=1"
            ).set_footer(text="Deleted message.")
            await msgobj.channel.send(embed=E)

    @commands.Cog.listener("on_message_edit")
    async def ghostping_edit(self, before, after):

        if len(before.mentions) == 0 or before.author.bot or before.content == after.content:
            return

        g = await self.client.get_guild_config(before.guild.id)
        if not g['ghost_ping']:
            return

        if before.edited_at is None:
            time_EB = int(before.created_at.strftime("%H%M%S"))
            time_EA = int(after.edited_at.strftime("%H%M%S"))
        else:
            time_EB = int(before.edited_at.strftime("%H%M%S"))
            time_EA = int(after.edited_at.strftime("%H%M%S"))

        string = ""
        delta = time_EA - time_EB
        if delta > 11:
            return

        if before.mention_everyone and not after.mention_everyone:
            string += " (@everyone / @here)"

        mentionsB = before.role_mentions
        for i in before.mentions:
            if not i.bot:
                if not i == before.author:
                    mentionsB.append(i)
        if mentionsB:
            mentionsA = after.role_mentions
            for i in after.mentions:
                if not i.bot:
                    if not i == after.author:
                        mentionsA.append(i)

            mentionsDelta = list(set(mentionsB) - set(mentionsA))
            for i in mentionsDelta:
                string += f"{i.mention} "

        if string:
            E = discord.Embed(
                title=f"{EMOJIS['hu_peng']} Ghost ping detected!",
                description=f"[Original Message]({after.jump_url})",
                color=RED_COLOR,
                timestamp=after.edited_at
            ).set_author(name=after.author, icon_url=after.author.display_avatar.url
            ).add_field(name="Offender:", value=after.author.mention, inline=False
            ).add_field(name="Victims:", value=string, inline=False
            ).set_thumbnail(url="https://cdn.discordapp.com/emojis/527884882010177536.png?v=1"
            ).set_footer(text="Edited message.")

            await after.reply(embed=E)


def setup(client):
    client.add_cog(Automod(client))

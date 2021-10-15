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
import typing as t

from discord.ext import commands
import emojis
from config import DEFAULT_BANNED_WORDS, EMOJIS, RED_COLOR, DEFAULT_AUTOMOD_CONFIG
from datetime import datetime
from re import search
from collections import Counter
from utils.bot import EpicBot
from utils.embed import error_embed, success_embed
from utils.ui import BasicView, Paginator, SelectWithMultipleOptions
from utils.exceptions import AutomodModuleNotEnabled


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

    def mod_perms(self, m: discord.Message) -> bool:
        p = m.author.guild_permissions
        return True if (p.kick_members or p.administrator or p.ban_members or p.manage_guild or m.author == m.guild.owner) else False

    @commands.Cog.listener("on_automod_trigger")
    async def on_automod_trigger(self, am_config: dict, message: discord.Message, module: str):
        lc_id = am_config.get('log_channel')
        if not lc_id:
            return
        log_channel = self.client.get_channel(lc_id)
        if not log_channel:
            return
        embed = error_embed(
            "⚠️ Automod triggered!",
            message.content
        ).add_field(name="Module:", value=module
        ).set_author(name=message.author, icon_url=message.author.display_avatar.url
        ).set_footer(text=f"Message ID: {message.id} | User ID: {message.author.id}")
        await log_channel.send(embed=embed)

    @commands.Cog.listener("on_message")
    async def efficient_automod(self, msg: discord.Message):
        if msg.author.bot or msg.content == "" or not msg.guild:
            return
        if self.mod_perms(msg):
            return
        g = await self.client.get_guild_config(msg.guild.id)
        am = g['automod']
        if msg.channel.id in am['ignored_channels']:
            return
        for r in msg.author.roles:
            if r.id in am['allowed_roles']:
                return

        checks = {
            'banned_words': self.banned_words,
            'all_caps': self.all_caps,
            'duplicate_text': self.duplicate_text,
            'message_spam': self.message_spam,
            'invites': self.invites,
            'links': self.links,
            'mass_mentions': self.mass_mentions,
            'emoji_spam': self.emoji_spam,
            'zalgo_text': self.zalgo_text,
        }

        for module, check in checks.items():
            if am[module]['enabled']:
                final = await check(msg, am[module])
                if final:
                    self.client.dispatch('automod_trigger', am_config=am, message=msg, module=module)
                    return

    async def banned_words(self, msg: discord.Message, m: dict) -> bool:
        guild_banned_words = DEFAULT_BANNED_WORDS.copy()
        removed_words = m.get('removed_words', [])
        for word in removed_words:
            guild_banned_words.remove(word)
        for w in guild_banned_words:
            if w in msg.content.lower():
                try:
                    await msg.delete()
                except Exception:
                    pass
                await msg.channel.send(
                    f"{msg.author.mention}, Watch your language.",
                    delete_after=5,
                    allowed_mentions=self.peng
                )
                return True
        for w in m['words']:
            if w in msg.content.lower():
                try:
                    await msg.delete()
                except Exception:
                    pass
                await msg.channel.send(
                    f"{msg.author.mention}, Watch your language.",
                    delete_after=5,
                    allowed_mentions=self.peng
                )
                return True
        return False

    async def all_caps(self, msg: discord.Message, m: dict) -> bool:
        if len(msg.content) <= 7:
            return False
        if msg.content.isupper():
            try:
                await msg.delete()
            except Exception:
                pass
            await msg.channel.send(
                f"{msg.author.mention}, Too many caps.",
                delete_after=5,
                allowed_mentions=self.peng
            )
            return True
        upper_count = 0
        for h in msg.content:
            if h.isupper():
                upper_count += 1
        if (upper_count / len(msg.content)) * 100 > 70:
            await msg.delete()
            await msg.channel.send(
                f"{msg.author.mention}, Too many caps.",
                delete_after=5,
                allowed_mentions=self.peng
            )
            return True
        return False

    async def duplicate_text(self, msg: discord.Message, m: dict) -> bool:
        if len(msg.content) < 100:
            return False
        c_ = Counter(msg.content.lower())
        for c, n in c_.most_common(None):
            if c != ' ' and len(msg.content) / n < 9:
                await msg.delete()
                await msg.channel.send(
                    f"{msg.author.mention}, No spamming.",
                    delete_after=5,
                    allowed_mentions=self.peng
                )
                return True
        return False

    async def message_spam(self, msg: discord.Message, m: dict) -> bool:
        def _check(m):
            return (m.author == msg.author and (datetime.utcnow() - m.created_at.replace(tzinfo=None)).seconds < 7)
        h = list(filter(lambda m: _check(m), self.client.cached_messages))
        if len(h) >= 5:
            await msg.channel.purge(limit=5, check=_check)
            await msg.channel.send(
                f"{msg.author.mention}, Stop spamming.",
                delete_after=5,
                allowed_mentions=self.peng
            )
            return True
        return False

    async def invites(self, msg: discord.Message, m: dict) -> bool:
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
                        await msg.channel.send(
                            f"{msg.author.mention}, No invite links.",
                            delete_after=5,
                            allowed_mentions=self.peng
                        )
                        return True
        return False

    async def links(self, msg: discord.Message, m: dict) -> bool:
        whitelisted_links = [link.replace("https://", "").replace("http://", "").replace("www.", "") for link in m['whitelist']]
        kek = msg.content
        for link in whitelisted_links:
            kek = kek.replace(f"https://{link}", "").replace(f"www.{link}", "").replace(f"http://{link}", "").replace(f"http://www.{link}", "")

        if search(self.url_regex, kek):
            await msg.delete()
            await msg.channel.send(
                f"{msg.author.mention}, No links allowed.",
                delete_after=5,
                allowed_mentions=self.peng
            )
            return True
        return False

    async def mass_mentions(self, msg: discord.Message, m: dict) -> bool:
        if len(msg.mentions) >= 3:
            await msg.delete()
            await msg.channel.send(
                f"{msg.author.mention}, Don't spam mentions.",
                delete_after=5,
                allowed_mentions=self.peng
            )
            return True
        return False

    async def emoji_spam(self, msg: discord.Message, m: dict) -> bool:
        converter = commands.PartialEmojiConverter()
        stuff = msg.content.split()
        emoji_count = emojis.count(msg.content)
        ctx = await self.client.get_context(msg)
        for thing in stuff:
            try:
                await converter.convert(ctx, thing)
                emoji_count += 1
            except commands.PartialEmojiConversionFailure:
                pass
        if emoji_count > 10:
            await msg.delete()
            await msg.channel.send(
                f"{msg.author.mention}, Don't spam emojis.",
                delete_after=5,
                allowed_mentions=self.peng
            )
            return True
        return False

    async def zalgo_text(self, msg: discord.Message, m: dict) -> bool:
        x = self.zalgo_regex.search(urllib.parse.quote(msg.content.encode("utf-8")))
        if x:
            await msg.delete()
            await msg.channel.send(
                f"{msg.author.mention}, No zalgo allowed.",
                delete_after=5,
                allowed_mentions=self.peng
            )
            return True
        return False

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


async def show_automod_config(ctx: commands.Context) -> t.Tuple[discord.Embed, discord.ui.View]:
    g = await ctx.bot.get_guild_config(ctx.guild.id)
    am = g['automod']
    tick_yes = EMOJIS['tick_yes']
    tick_no = EMOJIS['tick_no']
    cancer = ['ignored_channels', 'allowed_roles', 'log_channel']
    lc_id = am.get('log_channel')
    log_channel = f"<#{lc_id}>" if lc_id is not None else "No log channel set."
    embed1 = success_embed(
        "Automod Filters Configuration",
        f"**Here are all the automod filters status:**\n\nLog channel: {log_channel}"
    )
    embed2 = success_embed(
        "Automod Whitelist Configuration",
        "**Here are all the automod whitelist configuration:**"
    ).add_field(name="Whitelisted Roles:", value=" ".join([f"<@&{r}>" for r in am['allowed_roles']]) or "No roles.", inline=False
    ).add_field(name="Whitelisted Channels:", value=" ".join([f"<#{c}>" for c in am['ignored_channels']]) or "No channels.", inline=False)
    for e in am:
        if e not in cancer:
            embed1.add_field(
                name=f"**{e.replace('_', ' ').title()}**",
                value=tick_yes + ' Enabled' if am[e]['enabled'] else tick_no + ' Disabled'
            )
    view = AutomodConfigView(ctx=ctx, embeds=[embed1, embed2])
    return embed1, view


async def am_add_badwords(ctx: commands.Context, *words: str) -> t.Tuple[t.List[str], t.List[str]]:
    g = await ctx.bot.get_guild_config(ctx.guild.id)
    am = g['automod']
    enabled = True if am['banned_words']['enabled'] else False
    if not enabled:
        raise AutomodModuleNotEnabled('banned_words')

    already_exist = []
    added = []

    for word in words:
        if word in DEFAULT_BANNED_WORDS:
            if word in am['banned_words'].get('removed_words', []):
                am['banned_words']['removed_words'].remove(word)
                added.append(word)
            else:
                already_exist.append(word)
        elif word in am['banned_words']['words']:
            already_exist.append(word)
        else:
            am['banned_words']['words'].append(word)
            added.append(word)

    return added, already_exist


async def am_remove_badwords(ctx: commands.Context, *words: str) -> t.Tuple[t.List[str], t.List[str]]:
    g = await ctx.bot.get_guild_config(ctx.guild.id)
    am = g['automod']
    enabled = True if am['banned_words']['enabled'] else False
    if not enabled:
        raise AutomodModuleNotEnabled('banned_words')

    not_exist = []
    removed = []

    for word in words:
        if word in DEFAULT_BANNED_WORDS:
            if 'removed_words' not in am['banned_words']:
                am['banned_words'].update({"removed_words": []})
            if word not in am['banned_words']['removed_words']:
                am['banned_words']['removed_words'].append(word)
                removed.append(word)
            else:
                not_exist.append(word)
        elif word not in am['banned_words']['words']:
            not_exist.append(word)
        else:
            am['banned_words']['words'].remove(word)
            removed.append(word)

    return removed, not_exist


async def view_badword_list(ctx: commands.Context) -> t.Tuple[discord.Embed, t.Optional[discord.ui.View]]:
    g = await ctx.bot.get_guild_config(ctx.guild.id)
    am = g['automod']
    enabled = True if am['banned_words']['enabled'] else False
    if not enabled:
        raise AutomodModuleNotEnabled('banned_words')
    paginator = commands.Paginator(prefix="", suffix="", max_size=500)
    banned_list = [word for word in am['banned_words']['words']]
    for wrd in DEFAULT_BANNED_WORDS:
        if wrd.lower() not in am['banned_words'].get('removed_words', []):
            banned_list.append(wrd.lower())
    i = 1
    if len(banned_list) != 0:
        for badword in banned_list:
            paginator.add_line(f"{i} - `{badword}`")
            i += 1
    else:
        paginator.add_line("There are no bad words added for this server!")
    all_embeds = [success_embed("All Bad Words", page) for page in paginator.pages]
    view = Paginator(ctx, all_embeds) if len(all_embeds) != 1 else None
    return all_embeds[0], view


async def am_whitelist_func(ctx: commands.Context, choice: bool, setting: t.Optional[t.Union[discord.Role, discord.TextChannel]]) -> bool:
    g = await ctx.bot.get_guild_config(ctx.guild.id)
    am = g['automod']
    if choice:
        if isinstance(setting, discord.TextChannel):
            if setting.id in am['ignored_channels']:
                return False
            am['ignored_channels'].append(setting.id)
            return True
        else:
            if setting.id in am['allowed_roles']:
                return False
            am['allowed_roles'].append(setting.id)
            return True
    else:
        if isinstance(setting, discord.TextChannel):
            if setting.id not in am['ignored_channels']:
                return False
            am['ignored_channels'].remove(setting.id)
            return True
        else:
            if setting.id not in am['allowed_roles']:
                return False
            am['allowed_roles'].remove(setting.id)
            return True


async def link_add_to_whitelist(ctx: commands.Context, url: str) -> bool:
    g = await ctx.bot.get_guild_config(ctx.guild.id)
    am = g['automod']
    enabled = True if am['links']['enabled'] else False
    if not enabled:
        raise AutomodModuleNotEnabled('links')
    if url in am['links']['whitelist']:
        return False
    else:
        am['links']['whitelist'].append(url)
        return True


async def link_remove_from_whitelist(ctx: commands.Context, url: str = None) -> bool:
    g = await ctx.bot.get_guild_config(ctx.guild.id)
    am = g['automod']
    enabled = True if am['links']['enabled'] else False
    if not enabled:
        raise AutomodModuleNotEnabled('links')
    if url not in am['links']['whitelist']:
        return False
    else:
        am['links']['whitelist'].remove(url)
        return True


async def view_whitelisted_links_list(ctx: commands.Context) -> t.Tuple[discord.Embed, discord.ui.View]:
    g = await ctx.bot.get_guild_config(ctx.guild.id)
    am = g['automod']
    enabled = True if am['links']['enabled'] else False
    if not enabled:
        raise AutomodModuleNotEnabled('links')
    paginator = commands.Paginator(prefix="", suffix="", max_size=500)
    whitelisted_list = [url for url in am['links']['whitelist']]
    i = 1
    if len(whitelisted_list) != 0:
        for url in whitelisted_list:
            paginator.add_line(f"{i} - `{url}`")
            i += 1
    else:
        paginator.add_line("There are no whitelisted links added for this server!")
    all_embeds = [success_embed("All Whitelisted Links", page) for page in paginator.pages]

    view = Paginator(ctx, all_embeds) if len(all_embeds) != 1 else None
    return all_embeds[0], view


async def am_enable_a_module(ctx: commands.Context, module: str = None) -> None:
    g = await ctx.bot.get_guild_config(ctx.guild.id)
    am = g['automod']
    m_conf = am[module]
    m_conf['enabled'] = True
    am.update({module: m_conf})


async def am_enable_module_dropdown(ctx: commands.Context) -> t.Tuple[discord.Embed, discord.ui.View]:
    g = await ctx.bot.get_guild_config(ctx.guild.id)
    am = g['automod']
    view = BasicView(ctx, None)
    select = SelectWithMultipleOptions("Please select an automod module.", [module for module in DEFAULT_AUTOMOD_CONFIG if isinstance(DEFAULT_AUTOMOD_CONFIG[module], dict)])
    button = discord.ui.Button(style=discord.ButtonStyle.blurple, label="Continue")
    cancel_btn = discord.ui.Button(style=discord.ButtonStyle.danger, label="Cancel")

    async def button_callback(interaction: discord.Interaction):
        if not select.values:
            return await interaction.response.send_message("Please select some automod modules first.", ephemeral=True)
        for value in select.values:
            current_module = am[value]
            current_module['enabled'] = True
            am.update({value: current_module})
        return await interaction.message.edit(embed=success_embed(
            f"{EMOJIS['tick_yes']} Modules enabled!",
            f"The following automod modules have been enabled: {', '.join([f'`{v_}`' for v_ in select.values])}"
        ), view=None)

    async def cancel_callback(interaction):
        await interaction.message.delete()

    button.callback = button_callback
    cancel_btn.callback = cancel_callback

    view.add_item(select)
    view.add_item(button)
    view.add_item(cancel_btn)
    embed = success_embed(
        f"{EMOJIS['loading']} Enabling automod modules...",
        "Please select a few modules to enable and then click `Continue`"
    )
    return embed, view


async def am_disable_modules(ctx: commands.Context, *modules: str) -> None:
    g = await ctx.bot.get_guild_config(ctx.guild.id)
    for module in modules:
        am = g['automod']
        m_conf = am[module]
        m_conf['enabled'] = False
        am.update({module: m_conf})


class AutomodConfigView(discord.ui.View):
    def __init__(self, ctx: commands.Context, embeds: list):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.embeds = embeds

    @discord.ui.button(label="Filters Config", style=discord.ButtonStyle.blurple, disabled=True)
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

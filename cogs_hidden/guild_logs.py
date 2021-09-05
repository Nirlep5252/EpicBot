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
import datetime

from discord.ext import commands
from discord.utils import escape_markdown
from humanfriendly import format_timespan
from config import (
    EMOJIS, MAIN_COLOR, RED_COLOR
)
from utils.bot import EpicBot
from typing import List


class GuildLogs(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client
        self.no_mentions = discord.AllowedMentions.none()

    async def check_enabled(self, guild_id):
        g = await self.client.get_guild_config(guild_id)
        if g['logging'] is None:
            return False
        else:
            return g

    async def get_log_webhook(self, e):
        channel = self.client.get_channel(e)
        webhooks = await channel.webhooks()
        w = discord.utils.get(webhooks, name="EpicBot Logs", user=self.client.user)
        if w is None:
            w = await channel.create_webhook(name="EpicBot Logs")
        return w

    async def send_from_webhook(self, webhook: discord.Webhook, embed: discord.Webhook, files: List[discord.File] = [], embeds: List[discord.Embed] = []):
        if embed is None:
            await webhook.send(
                allowed_mentions=self.no_mentions,
                avatar_url=self.client.user.display_avatar.url,
                files=files,
                embeds=embeds
            )
        else:
            await webhook.send(
                embed=embed,
                allowed_mentions=self.no_mentions,
                avatar_url=self.client.user.display_avatar.url,
                files=files
            )

    @commands.Cog.listener("on_member_join")
    async def send_join_log(self, member: discord.Member):
        g = await self.check_enabled(member.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])

        e = discord.Embed(
            description=f"{member.mention} {escape_markdown(str(member))}",
            timestamp=datetime.datetime.utcnow(),
            color=MAIN_COLOR
        ).set_author(name="Member Joined!", icon_url=member.display_avatar.url
        ).add_field(
            name="Account Age",
            value=format_timespan((datetime.datetime.utcnow() - member.created_at.replace(tzinfo=None)).total_seconds()),
            inline=False
        ).set_footer(text=f"ID: {member.id}"
        ).set_thumbnail(url=member.display_avatar.url)
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_member_remove")
    async def send_leave_log(self, member: discord.Member):
        g = await self.check_enabled(member.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])

        e = discord.Embed(
            description=f"{member.mention} {escape_markdown(str(member))}",
            timestamp=datetime.datetime.utcnow(),
            color=RED_COLOR
        ).set_author(name="Member Left!", icon_url=member.display_avatar.url
        ).set_footer(text=f"ID: {member.id}", icon_url=member.display_avatar.url
        ).set_thumbnail(url=member.display_avatar.url)

        roles = ""
        for role in member.roles[::-1]:
            if len(roles) > 500:
                roles += "and more roles..."
                break
            if str(role) != "@everyone":
                roles += f"{role.mention} "
        if len(roles) == 0:
            roles = "No roles."

        e.add_field(
            name="Roles:",
            value=roles,
            inline=False
        )
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_member_ban")
    async def send_ban_log(self, guild, user):
        g = await self.check_enabled(guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])

        e = discord.Embed(
            description=f"{user.mention} {escape_markdown(str(user))}",
            timestamp=datetime.datetime.utcnow(),
            color=RED_COLOR
        ).set_author(name="Member Banned!", icon_url=user.display_avatar.url
        ).set_footer(text=f"ID: {user.id}"
        ).set_thumbnail(url=user.display_avatar.url)

        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_member_unban")
    async def send_unban_log(self, guild, user):
        g = await self.check_enabled(guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])

        e = discord.Embed(
            description=f"{user.mention} {escape_markdown(str(user))}",
            timestamp=datetime.datetime.utcnow(),
            color=MAIN_COLOR
        ).set_author(name="Member Unbanned!", icon_url=user.display_avatar.url
        ).set_footer(text=f"ID: {user.id}"
        ).set_thumbnail(url=user.display_avatar.url)

        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_message_delete")
    async def send_del_msg(self, msg: discord.Message):
        if msg.author.bot:
            return
        g = await self.check_enabled(msg.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])

        f = []
        for f_ in msg.attachments:
            f.append(await f_.to_file())

        e = discord.Embed(
            title="Message deleted!",
            description=msg.content,
            timestamp=datetime.datetime.utcnow(),
            color=RED_COLOR
        ).set_author(name=f"{msg.author} ({msg.author.id})", icon_url=msg.author.display_avatar.url
        ).set_footer(text=f"Message ID: {msg.id}"
        ).add_field(name="Channel:", value=msg.channel.mention, inline=False
        ).set_thumbnail(url=msg.author.display_avatar.url)

        for sticker in msg.stickers:
            e.add_field(
                name=f"Sticker: `{sticker.name}`",
                value=f"ID: [`{sticker.id}`]({sticker.url})"
            )
        if len(msg.stickers) == 1:
            e.set_image(url=msg.stickers[0].url)

        await self.send_from_webhook(w, e, f)

    @commands.Cog.listener("on_message_edit")
    async def send_edit_msg(self, before: discord.Message, after: discord.Message):
        if before.author.bot:
            return
        if before.content == after.content and len(before.attachments) == 0:
            return
        g = await self.check_enabled(before.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])

        f = []
        for f_ in before.attachments:
            f.append(await f_.to_file())

        e = discord.Embed(
            title="Message edited!",
            description=f"**Message edited in {before.channel.mention}**\n[Jump to message!]({before.jump_url})",
            timestamp=datetime.datetime.utcnow(),
            color=MAIN_COLOR
        ).set_author(name=f"{before.author} ({before.author.id})", icon_url=before.author.display_avatar.url
        ).set_footer(text=f"Message ID: {before.id}"
        ).set_thumbnail(url=before.author.display_avatar.url)
        e1 = discord.Embed(
            title="Before:",
            description=before.content,
            color=MAIN_COLOR
        )
        e2 = discord.Embed(
            title="After:",
            description=after.content,
            color=MAIN_COLOR
        )
        await self.send_from_webhook(w, None, f, [e, e1, e2])

    @commands.Cog.listener("on_bulk_message_delete")
    async def send_bulk_delete_log(self, messages):
        g = await self.check_enabled(messages[0].guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])
        e = discord.Embed(
            description=f"**Bulk delete in {messages[0].channel.mention}, {len(messages)} messages deleted.**",
            timestamp=datetime.datetime.utcnow(),
            color=RED_COLOR
        ).set_author(name=messages[0].guild, icon_url=messages[0].guild.icon.url)
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_guild_channel_create")
    async def send_channel_create_log(self, channel):
        g = await self.check_enabled(channel.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])
        e = discord.Embed(
            description=f"**Channel created: `#{channel.name}`**",
            timestamp=datetime.datetime.utcnow(),
            color=MAIN_COLOR
        ).set_author(name=channel.guild, icon_url=channel.guild.icon.url
        ).set_footer(text=f"ID: {channel.id}")
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_guild_channel_delete")
    async def send_channel_delete_log(self, channel):
        g = await self.check_enabled(channel.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])
        e = discord.Embed(
            description=f"**Channel deleted: `#{channel.name}`**",
            timestamp=datetime.datetime.utcnow(),
            color=RED_COLOR
        ).set_author(name=channel.guild, icon_url=channel.guild.icon.url
        ).set_footer(text=f"ID: {channel.id}")
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_guild_channel_update")
    async def send_channel_update_log(self, before, after):
        if before.position - after.position in [1, -1]:
            return
        g = await self.check_enabled(before.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])
        e = discord.Embed(
            description=f"**Channel updated: {after.mention}**",
            timestamp=datetime.datetime.utcnow(),
            color=MAIN_COLOR
        ).set_author(name=after.guild, icon_url=after.guild.icon.url
        ).set_footer(text=f"ID: {after.id}")
        if before.name != after.name:
            e.add_field(
                name="Name:",
                value=f"`{before.name}` ➜ `{after.name}`",
                inline=False
            )
        if before.category != after.category:
            e.add_field(
                name="Category:",
                value=f"`{before.category}` ➜ `{after.category}`",
                inline=False
            )
        if before.permissions_synced != after.permissions_synced:
            e.add_field(
                name="Permissions Synced:",
                value=f"`{before.permissions_synced}` ➜ `{after.permissions_synced}`",
                inline=False
            )
        if before.position != after.position:
            e.add_field(
                name="Position changed:",
                value=f"`{before.position}` ➜ `{after.position}`",
                inline=False
            )
        if isinstance(before, discord.TextChannel) and before.topic != after.topic:
            e.add_field(
                name="Topic updated:",
                value=f"```{before.topic}``` ➜ ```{after.topic}```",
                inline=False
            )
        if isinstance(before, discord.TextChannel) and before.slowmode_delay != after.slowmode_delay:
            e.add_field(
                name="Slowmode changed:",
                value=f"`{format_timespan(before.slowmode_delay)}` ➜ `{format_timespan(after.slowmode_delay)}`",
                inline=False
            )
        if isinstance(before, discord.TextChannel) and before.is_nsfw() != after.is_nsfw():
            e.add_field(
                name="NSFW channel:",
                value=f"`{before.is_nsfw()}` ➜ `{after.is_nsfw()}`",
                inline=False
            )
        if isinstance(before, discord.TextChannel) and before.is_news() != after.is_news():
            e.add_field(
                name="Announcement channel:",
                value=f"`{before.is_news()}` ➜ `{after.is_news()}`",
                inline=False
            )
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_guild_role_create")
    async def role_create_log(self, role):
        g = await self.check_enabled(role.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])
        e = discord.Embed(
            description=f"**Role created: `{role.name}`**",
            timestamp=datetime.datetime.utcnow(),
            color=MAIN_COLOR
        ).set_author(name=role.guild, icon_url=role.guild.icon.url
        ).set_footer(text=f"ID: {role.id}")
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_guild_role_delete")
    async def role_delete_log(self, role):
        g = await self.check_enabled(role.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])
        e = discord.Embed(
            description=f"**Role deleted: `{role.name}`**",
            timestamp=datetime.datetime.utcnow(),
            color=RED_COLOR
        ).set_author(name=role.guild, icon_url=role.guild.icon.url
        ).set_footer(text=f"ID: {role.id}")
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_guild_role_update")
    async def role_update_log(self, before, after):
        if before.position - after.position in [1, -1]:
            return
        g = await self.check_enabled(before.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])
        e = discord.Embed(
            description=f"**Role updated: {after.mention}**",
            timestamp=datetime.datetime.utcnow(),
            color=MAIN_COLOR
        ).set_author(name=after.guild, icon_url=after.guild.icon.url
        ).set_footer(text=f"ID: {after.id}")
        if before.color != after.color:
            e.add_field(
                name="Color:",
                value=f"`{before.color}` ➜ `{after.color}`",
                inline=False
            )
        if before.hoist != after.hoist:
            e.add_field(
                name="Hoisted:",
                value=f"`{before.hoist}` ➜ `{after.hoist}`",
                inline=False
            )
        if before.mentionable != after.mentionable:
            e.add_field(
                name="Mentionable:",
                value=f"`{before.mentionable}` ➜ `{after.mentionable}`",
                inline=False
            )
        if before.name != after.name:
            e.add_field(
                name="Name:",
                value=f"`{before.name}` ➜ `{after.name}`",
                inline=False
            )
        if before.position != after.position:
            e.add_field(
                name="Position:",
                value=f"`{before.position}` ➜ `{after.position}`",
                inline=False
            )
        if before.permissions != after.permissions:
            hehe_ = ""

            before_perms = {}
            after_perms = {}

            for h, H in before.permissions:
                before_perms.update({h: H})
            for p, P in after.permissions:
                after_perms.update({p: P})

            for g in before_perms:
                if before_perms[g] != after_perms[g]:
                    hehe_ += f"**{' '.join(g.split('_')).title()}:** `{before_perms[g]}` ➜ `{after_perms[g]}`\n"

            e.add_field(
                name="Permissions:",
                value=hehe_,
                inline=False
            )
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_member_update")
    async def member_roles_update_log(self, before, after):
        if before.roles == after.roles:
            return
        g = await self.check_enabled(before.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])
        roles = []
        role_text = ""
        if len(before.roles) > len(after.roles):
            for e in before.roles:
                if e not in after.roles:
                    roles.append(e)
        else:
            for e in after.roles:
                if e not in before.roles:
                    roles.append(e)
        for h in roles:
            role_text += f"`{h.name}`, "
        role_text = role_text[:-2]
        e = discord.Embed(
            description=f"Role{'s' if len(roles) > 1 else ''} {role_text} {'were' if len(roles) > 1 else 'was'} {'added to' if len(before.roles) < len(after.roles) else 'removed from'} {after.mention}",
            timestamp=datetime.datetime.utcnow(),
            color=RED_COLOR if len(before.roles) > len(after.roles) else MAIN_COLOR
        ).set_author(name=after, icon_url=after.display_avatar.url
        ).set_footer(text=f"ID: {after.id}")
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_member_update")
    async def member_nickname_log(self, before, after):
        if before.nick == after.nick:
            return
        g = await self.check_enabled(before.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])
        e = discord.Embed(
            title="Nickname updated:",
            description=f"`{before.nick}` ➜ `{after.nick}`",
            timestamp=datetime.datetime.utcnow(),
            color=MAIN_COLOR
        ).set_author(name=after, icon_url=after.display_avatar.url
        ).set_footer(text=f"ID: {after.id}")
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_voice_state_update")
    async def member_join_leave_vc(self, member, before, after):
        if before.channel == after.channel:
            return
        g = await self.check_enabled(member.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])
        if before.channel is None:
            e = discord.Embed(
                description=f"**{member.mention} joined voice channel {after.channel.mention}**",
                timestamp=datetime.datetime.utcnow(),
                color=MAIN_COLOR
            )
        elif after.channel is None:
            e = discord.Embed(
                description=f"**{member.mention} left voice channel {before.channel.mention}**",
                timestamp=datetime.datetime.utcnow(),
                color=RED_COLOR
            )
        else:
            e = discord.Embed(
                description=f"**{member.mention} switched voice channel {before.channel.mention} ➜ {after.channel.mention}**",
                timestamp=datetime.datetime.utcnow(),
                color=MAIN_COLOR
            )
        e.set_author(name=member, icon_url=member.display_avatar.url)
        e.set_footer(text=f"ID: {member.id}")
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_guild_emojis_update")
    async def guild_emojis_updated_log(self, guild, before, after):
        if before == after:
            return
        g = await self.check_enabled(guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])
        emojis_added = ""
        emojis_removed = ""
        for e in before:
            if e not in after:
                emojis_removed += f"`{e.name}` "
        for E in after:
            if E not in before:
                emojis_added += f"{E} "
        e = discord.Embed(
            title="Server emojis updated",
            timestamp=datetime.datetime.utcnow(),
            color=MAIN_COLOR
        ).set_author(name=guild, icon_url=guild.icon.url
        ).set_footer(text=f"ID: {guild.id}")
        if emojis_added != "":
            e.add_field(
                name="Emojis added:",
                value=emojis_added,
                inline=False
            )
        if emojis_removed != "":
            e.add_field(
                name="Emojis Removed:",
                value=emojis_removed,
                inline=False
            )
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_guild_update")
    async def guild_update_log(self, before: discord.Guild, after: discord.Guild):
        g = await self.check_enabled(before.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])
        e = discord.Embed(
            description="**Server updated**",
            timestamp=datetime.datetime.utcnow(),
            color=MAIN_COLOR
        ).set_author(name=after, icon_url=after.icon.url
        ).set_footer(text=f"ID: {after.id}")
        if before.afk_channel != after.afk_channel:
            e.add_field(
                name="AFK Channel:",
                value=f"`{before.afk_channel}` ➜ `{after.afk_channel}`",
                inline=False
            )
        if before.afk_timeout != after.afk_timeout:
            e.add_field(
                name="AFK Timeout:",
                value=f"`{format_timespan(before.afk_timeout)}` ➜ `{format_timespan(after.afk_timeout)}`",
                inline=False
            )
        if before.banner != after.banner:
            e.add_field(
                name="Banner updated!",
                value=f"{'`None`' if before.banner is None else '[`Before`]('+str(before.banner.url)+')'} ➜ {'`None`' if after.banner is None else '[`After`]('+str(after.banner.url)+')'}",
                inline=False
            )
        if before.default_notifications != after.default_notifications:
            e.add_field(
                name="Default Notifications:",
                value=f"`{before.default_notifications}` ➜ `{after.default_notifications}`",
                inline=False
            )
        if before.description != after.description:
            e.add_field(
                name="Description:",
                value=f"```{before.description}``` ➜ ```{after.description}```",
                inline=False
            )
        if before.icon != after.icon:
            e.add_field(
                name="Icon:",
                value=f"{'`None`' if before.icon is None else '[`Before`]('+str(before.icon.url)+')'} ➜ {'`None`' if after.icon is None else '[`After`]('+str(after.icon.url)+')'}",
                inline=False
            )
        if before.mfa_level != after.mfa_level:
            e.add_field(
                name="2FA Requirement:",
                value=f"`{'True' if before.mfa_level == 1 else 'False'}` ➜ `{'True' if after.mfa_level == 1 else 'False'}`",
                inline=False
            )
        if before.name != after.name:
            e.add_field(
                name="Name:",
                value=f"`{before.name}` ➜ `{after.name}`",
                inline=False
            )
        if before.owner != after.owner:
            e.add_field(
                name="Owner:",
                value=f"`{before.owner}` ➜ `{after.owner}`",
                inline=False
            )
        if before.public_updates_channel != after.public_updates_channel:
            e.add_field(
                name="Mod new channel:",
                value=f"`{before.public_updates_channel}` ➜ `{after.public_updates_channel}`",
                inline=False
            )
        if before.region != after.region:
            e.add_field(
                name="Region:",
                value=f"`{before.region}` ➜ `{after.region}`",
                inline=False
            )
        if before.rules_channel != after.rules_channel:
            e.add_field(
                name="Rules channel:",
                value=f"`{before.rules_channel}` ➜ `{after.rules_channel}`",
                inline=False
            )
        if before.splash != after.splash:
            e.add_field(
                name="Invite splash banner:",
                value=f"{'`None`' if before.splash is None else '[`Before`]('+str(before.splash.url)+')'} ➜ {'`None`' if after.splash is None else '[`After`]('+str(after.splash.url)+')'}",
                inline=False
            )
        if before.system_channel != after.system_channel:
            e.add_field(
                name="System channel:",
                value=f"`{before.system_channel}` ➜ `{after.system_channel}`",
                inline=False
            )
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_thread_join")
    async def thread_created_or_joined(self, thread: discord.Thread):
        g = await self.check_enabled(thread.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])
        e = discord.Embed(
            description=f"""
**Thread created: {thread.mention} `#{thread.name}`**

**Private:** {EMOJIS['tick_no'] if thread.type.name == "private_thread" else EMOJIS['tick_yes']}
**Archived:** {EMOJIS['tick_yes'] if thread.archived else EMOJIS['tick_no']}
            """,
            timestamp=datetime.datetime.utcnow(),
            color=MAIN_COLOR
        ).set_author(name=thread.owner, icon_url=thread.owner.display_avatar.url if thread.owner is not None else "https://amogus.org/amogus.png"
        ).set_footer(text=f"ID: {thread.id}"
        ).add_field(name="Auto Archive Duration:", value=format_timespan(thread.auto_archive_duration), inline=False)
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_thread_delete")
    async def thread_deleted_log(self, thread: discord.Thread):
        g = await self.check_enabled(thread.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])
        e = discord.Embed(
            description=f"""
**Thread deleted: `#{thread.name}`**

**Private:** {EMOJIS['tick_no'] if thread.type.name == "private_thread" else EMOJIS['tick_yes']}
**Archived:** {EMOJIS['tick_yes'] if thread.archived else EMOJIS['tick_no']}
            """,
            timestamp=datetime.datetime.utcnow(),
            color=RED_COLOR
        ).set_author(name=thread.owner, icon_url=thread.owner.display_avatar.url if thread.owner is not None else "https://amogus.org/amogus.png"
        ).set_footer(text=f"ID: {thread.id}")
        await self.send_from_webhook(w, e)

    @commands.Cog.listener("on_thread_update")
    async def thread_update_log(self, before: discord.Thread, after: discord.Thread):
        g = await self.check_enabled(after.guild.id)
        if not g:
            return
        w = await self.get_log_webhook(g['logging'])
        e = discord.Embed(
            description="**Thread updated**",
            color=MAIN_COLOR,
            timestamp=datetime.datetime.utcnow()
        ).set_author(name=after.owner, icon_url=after.owner.display_avatar.url if after.owner is not None else "https://amogus.org/amogus.png"
        ).set_footer(text=f"ID: {after.id}")

        if before.archived != after.archived:
            e.add_field(name="Archived:", value=f"`{before.archived}` ➜ `{after.archived}`", inline=False)
        if before.auto_archive_duration != after.auto_archive_duration:
            e.add_field(name="Auto Archive Duration:", value=f"`{format_timespan(before.auto_archive_duration)}` ➜ `{format_timespan(after.auto_archive_duration)}`", inline=False)
        if before.name != after.name:
            e.add_field(name="Name:", value=f"`{before.name}` ➜ `{after.name}`", inline=False)
        if before.slowmode_delay != after.slowmode_delay:
            e.add_field(name="Slowmode:", value=f"`{format_timespan(before.slowmode_delay)}` ➜ `{format_timespan(after.slowmode_delay)}`", inline=False)

        await self.send_from_webhook(w, e)

# ---------- custom events ----------

    # @commands.Cog.listener("on_member_kick")
    # async def member_kick_log(self, member: discord.Member, entry: discord.AuditLogEntry):
    #     g = await self.check_enabled(member.guild.id)
    #     if not g:
    #         return
    #     w = await self.get_log_webhook(g['logging'])

    #     e = discord.Embed(
    #         description=f"{member.mention} {escape_markdown(str(member))} has been kicked by {entry.user.mention} {escape_markdown(str(entry.user))}",
    #         color=RED_COLOR,
    #         timestamp=datetime.datetime.utcnow()
    #     ).set_author(name=member, icon_url=member.display_avatar.url
    #     ).set_footer(icon_url=member.display_avatar.url, text=f"ID: {member.guild.id}"
    #     ).set_thumbnail(url=member.display_avatar.url
    #     ).add_field(name='Reason:', value=entry.reason or 'No reason provided.', inline=False)

    #     await self.send_from_webhook(w, e)


def setup(client):
    client.add_cog(GuildLogs(client))

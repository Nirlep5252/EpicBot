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

from typing import Union
from config import EPICBOT_GUILD_ID, STAFF_ROLE, OWNER_ROLE
import discord
import json

from discord.ext import commands
from utils.embed import process_embeds_from_json, replace_things_in_string_fancy_lemao
from utils.bot import EpicBot


class InviteTracking(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client

    def find_invite_by_code(self, inv_list, code):
        for inv in inv_list:
            if inv.code == code:
                return inv
        return 'pain'

    @commands.Cog.listener(name="on_invite_delete")
    async def updating_guild_invites_on_delete(self, invite: discord.Invite):
        g = await self.client.get_guild_config(invite.guild.id)
        if g['welcome']['channel_id'] is not None:
            await self.client.update_guild_before_invites(invite.guild.id)

    @commands.Cog.listener(name="on_invite_create")
    async def updating_guild_invites_on_create(self, invite: discord.Invite):
        g = await self.client.get_guild_config(invite.guild.id)
        if g['welcome']['channel_id'] is not None:
            await self.client.update_guild_before_invites(invite.guild.id)

    async def check_staff(self, user: Union[discord.Member, discord.User]):
        epicbot_guild = self.client.get_guild(EPICBOT_GUILD_ID)
        if epicbot_guild not in user.mutual_guilds:
            return False
        member = epicbot_guild.get_member(user.id)
        if epicbot_guild.get_role(OWNER_ROLE) in member.roles:
            return "owner"
        elif epicbot_guild.get_role(STAFF_ROLE) in member.roles:
            return "staff"
        return False

    @commands.Cog.listener(name="on_member_join")
    async def welcome_msg(self, member: discord.Member):
        guild = member.guild

        guild_config = await self.client.get_guild_config(guild.id)
        if guild_config['welcome']['channel_id'] is None:
            return
        old_invites = await self.client.get_guild_invites(guild.id)
        current_invites = await guild.invites()
        welcome_config = guild_config['welcome']
        channel_id = welcome_config['channel_id']
        embed = welcome_config['embed']

        inviter = "Unknown"
        if old_invites == 'pain':
            inviter = 'Unknown'
        else:
            for invite in old_invites:
                h = self.find_invite_by_code(current_invites, invite)
                if h != 'pain' and old_invites[invite] < h.uses and not member.bot:
                    inviter = self.find_invite_by_code(current_invites, invite).inviter.id
                    break
                else:
                    inviter = 'Unknown'

        await self.client.update_inviter(member.id, inviter, member.guild.id)
        await self.client.update_guild_before_invites(guild.id)
        if inviter != "Unknown":
            current_invites_of_user = await self.client.fetch_invites(inviter, guild.id, 'real')
            await self.client.update_invites(inviter, guild.id, 'real', current_invites_of_user + 1)

        channel = self.client.get_channel(channel_id)

        if channel is None:
            return

        staff = await self.check_staff(member)
        if embed:
            embed_json = json.loads(welcome_config['message'])
            things = await process_embeds_from_json(self.client, [member, guild], embed_json)

            if things[0] is not None:
                return await channel.send(things[0], embed=things[1])

            await channel.send(embed=things[1])
            if not staff:
                return
            else:
                if staff == 'owner':
                    await channel.send(f"{member.mention} is my mom 😊")
                elif staff == 'staff':
                    await channel.send(f"{member.mention} is a staff member 😊")
            return

        nice = await replace_things_in_string_fancy_lemao(self.client, [member, guild], welcome_config['message'])
        await channel.send(nice)
        if not staff:
            return
        else:
            if staff == 'owner':
                await channel.send(f"{member.mention} is my mom 😊")
            elif staff == 'staff':
                await channel.send(f"{member.mention} is an epicbot staff member 😊")
        return

    @commands.Cog.listener(name="on_member_remove")
    async def leave_msg(self, member: discord.Member):
        guild = member.guild

        guild_config = await self.client.get_guild_config(guild.id)
        leave_config = guild_config['leave']
        channel_id = leave_config['channel_id']
        embed = leave_config['embed']

        if guild_config['welcome']['channel_id'] is not None:
            inviter = await self.client.get_inviter(member.id, member.guild.id)

            await self.client.update_inviter(member.id, inviter, member.guild.id)
            await self.client.update_guild_before_invites(guild.id)
            if inviter != "Unknown":
                current_invites_of_user = await self.client.fetch_invites(inviter, guild.id, 'left')
                await self.client.update_invites(inviter, guild.id, 'left', current_invites_of_user + 1)

                current_invites_of_user = await self.client.fetch_invites(inviter, guild.id, 'real')
                await self.client.update_invites(inviter, guild.id, 'real', current_invites_of_user - 1)

        if guild_config['leave']['channel_id'] is None:
            return
        channel = self.client.get_channel(channel_id)

        if channel is None:
            return

        if embed:
            embed_json = json.loads(leave_config['message'])
            things = await process_embeds_from_json(self.client, [member, guild], embed_json)

            if things[0] is not None:
                return await channel.send(things[0], embed=things[1])

            return await channel.send(embed=things[1])

        nice = await replace_things_in_string_fancy_lemao(self.client, [member, guild], leave_config['message'])
        return await channel.send(nice)

    @commands.Cog.listener(name="on_member_join")
    async def autorole(self, member: discord.Member):
        guild_config = await self.client.get_guild_config(member.guild.id)
        if not guild_config['autorole']:
            return

        for e in guild_config['autorole']['all']:
            await member.add_roles(member.guild.get_role(e), reason="EpicBot Autorole!")

        if member.bot:
            for e in guild_config['autorole']['bots']:
                await member.add_roles(member.guild.get_role(e), reason="EpicBot Autorole!")

        if not member.bot:
            for e in guild_config['autorole']['humans']:
                await member.add_roles(member.guild.get_role(e), reason="EpicBot Autorole!")


def setup(client):
    client.add_cog(InviteTracking(client))

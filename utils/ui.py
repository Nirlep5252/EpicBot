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

import asyncio
import discord
from typing import Optional, Union, List
from discord.ext import commands
from discord import SelectOption


class Confirm(discord.ui.View):
    def __init__(self, context: commands.Context, timeout: Optional[int] = 300, user: Optional[Union[discord.Member, discord.User]] = None):
        super().__init__(timeout=timeout)
        self.value = None
        self.context = context
        self.user = user or self.context.author

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def yes(self, b, i):
        self.value = True
        self.stop()

    @discord.ui.button(label='No', style=discord.ButtonStyle.red)
    async def no(self, b, i):
        self.value = False
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            return await interaction.response.send_message("You cannot interact in other's commands.", ephemeral=True)
        return True


class Paginator(discord.ui.View):
    def __init__(self, ctx: commands.Context, embeds: List[discord.Embed]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.embeds = embeds
        self.current = 0

    async def edit(self, msg, pos):
        em = self.embeds[pos]
        em.set_footer(text=f"Page: {pos+1}")
        await msg.edit(embed=em)

    @discord.ui.button(emoji='◀️', style=discord.ButtonStyle.blurple)
    async def bac(self, b, i):
        if self.current == 0:
            return
        await self.edit(i.message, self.current - 1)
        self.current -= 1

    @discord.ui.button(emoji='⏹️', style=discord.ButtonStyle.blurple)
    async def stap(self, b, i):
        await i.message.delete()

    @discord.ui.button(emoji='▶️', style=discord.ButtonStyle.blurple)
    async def nex(self, b, i):
        if self.current + 1 == len(self.embeds):
            return
        await self.edit(i.message, self.current + 1)
        self.current += 1

    async def interaction_check(self, interaction):
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message("Not your command ._.", ephemeral=True)


class PaginatorText(discord.ui.View):
    def __init__(self, ctx: commands.Context, stuff: List[str]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.stuff = stuff
        self.current = 0

    async def edit(self, msg, pos):
        await msg.edit(content=self.stuff[pos])

    @discord.ui.button(emoji='◀️', style=discord.ButtonStyle.blurple)
    async def bac(self, b, i):
        if self.current == 0:
            return
        await self.edit(i.message, self.current - 1)
        self.current -= 1

    @discord.ui.button(emoji='⏹️', style=discord.ButtonStyle.blurple)
    async def stap(self, b, i):
        await i.message.delete()

    @discord.ui.button(emoji='▶️', style=discord.ButtonStyle.blurple)
    async def nex(self, b, i):
        if self.current + 1 == len(self.stuff):
            return
        await self.edit(i.message, self.current + 1)
        self.current += 1

    async def interaction_check(self, interaction):
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message("Not your command ._.", ephemeral=True)


class CloseOrClaimTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Claim', style=discord.ButtonStyle.blurple)
    async def claim(self, b: discord.ui.Button, i: discord.Interaction):
        b.disabled = True
        await i.message.edit(view=self)
        await i.channel.send(f'This ticket has been claimed by: {i.user.mention}')

    @discord.ui.button(label='Close', style=discord.ButtonStyle.red)
    async def close(self, b: discord.ui.Button, i: discord.Interaction):
        b.disabled = True
        await i.message.edit(view=self)
        await i.channel.send('Closing ticket...')
        await asyncio.sleep(2)
        await i.channel.edit(archived=True)


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def open_ticket(self, i):
        pass

    @discord.ui.button(label="Click to open ticket.", emoji='🎟️', custom_id='epicbot-tickets')
    async def ticket(self, button: discord.Button, interaction: discord.Interaction):
        for t in interaction.guild.threads:
            if t.name == f'ticket-{interaction.user.id}' and not t.archived:
                return await interaction.response.send_message(f'You already have a ticket {t.mention}', ephemeral=True)
        channel = interaction.channel
        thread = await channel.create_thread(name=f'ticket-{interaction.user.id}')
        await thread.send(
            f"📂 {interaction.user.mention} has created a ticket.",
            allowed_mentions=discord.AllowedMentions(
                everyone=False,
                roles=False,
                users=True,
                replied_user=False
            ),
            view=CloseOrClaimTicket()
        )


class SelfRoleOptionSelecter(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout: Optional[int] = 300):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.value = None

    @discord.ui.select(placeholder="Please select a selfrole option.", options=[
        SelectOption(label='Reactions', description="Users will react to get roles.", value='reaction'),
        SelectOption(label='Dropdowns', description="Users will select roles from a dropdown menu like this!", value='dropdown'),
        SelectOption(label='Buttons', description="Users will get roles by clicking buttons.", value='button')
    ])
    async def uwu(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.value = select.values[0]

    @discord.ui.button(label="Continue", style=discord.ButtonStyle.blurple)
    async def go_ahead(self, b: discord.Button, i: discord.Interaction):
        self.stop()

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def cancel(self, b: discord.Button, i: discord.Interaction):
        self.value = None
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            return False
        return True


class SelfRoleEditor(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout: Optional[int] = 300):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.value = None

    @discord.ui.select(placeholder="Please select an option to modify!", options=[
        SelectOption(label='Add', description="Add roles to the list.", value='add'),
        SelectOption(label='Remove', description="Remove roles from the list.", value='remove')
    ])
    async def uwu(self, select: discord.ui.Select, interaction: discord.Interaction):
        self.value = select.values[0]

    @discord.ui.button(label="Continue", style=discord.ButtonStyle.blurple)
    async def go_ahead(self, b: discord.Button, i: discord.Interaction):
        self.stop()

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def cancel(self, b: discord.Button, i: discord.Interaction):
        self.value = None
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            return False
        return True


class SelfRoleButton(discord.ui.Button):
    def __init__(self, guild: discord.Guild, emoji: str, role_id: int):
        super().__init__(emoji=emoji, style=discord.ButtonStyle.blurple, custom_id=str(role_id))
        self.guild = guild
        self.emoji = emoji
        self.role = guild.get_role(int(role_id))

    async def callback(self, interaction: discord.Interaction):
        if self.role is None:
            return
        if self.role in interaction.user.roles:
            await interaction.user.remove_roles(self.role, reason="EpicBot Selfroles")
            await interaction.response.send_message(f"Removed the {self.role.mention} role.", ephemeral=True)
        else:
            await interaction.user.add_roles(self.role, reason="EpicBot Selfroles")
            await interaction.response.send_message(f"Gave you the {self.role.mention} role.", ephemeral=True)


class ButtonSelfRoleView(discord.ui.View):
    def __init__(self, guild: discord.Guild, stuff: dict):
        super().__init__(timeout=None)
        for role_id, emoji in stuff.items():
            button = SelfRoleButton(guild, emoji, int(role_id))
            self.add_item(button)


class DropDownSelfRoleSelect(discord.ui.Select):
    def __init__(self, guild: discord.Guild, stuff: dict):
        options = []
        for role_id, emoji in stuff.items():
            role = guild.get_role(int(role_id))
            options.append(discord.SelectOption(label=role.name, emoji=emoji, value=str(role_id)))
        if len(options) == 1:
            options.append(discord.SelectOption(label="Remove role", emoji='❌', value='remove'))
        super().__init__(placeholder="Please select a role.", options=options, custom_id='selfrole-dropdown')
        self.guild = guild
        self.stuff = stuff

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'remove':
            role = self.guild.get_role(int(self.options[0].value))
            await interaction.user.remove_roles(role, reason="EpicBot Selfroles")
            await interaction.response.send_message(f"Removed the {role.mention} role.", ephemeral=True)
            return
        role = self.guild.get_role(int(self.values[0]))
        if role is None:
            return
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role, reason="EpicBot Selfroles")
            await interaction.response.send_message(f"Removed the {role.mention} role.", ephemeral=True)
        else:
            await interaction.user.add_roles(role, reason="EpicBot Selfroles")
            await interaction.response.send_message(f"Gave you the {role.mention} role.", ephemeral=True)


class DropDownSelfRoleView(discord.ui.View):
    def __init__(self, guild: discord.Guild, stuff: dict):
        super().__init__(timeout=None)
        self.add_item(DropDownSelfRoleSelect(guild, stuff))

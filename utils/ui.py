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
from typing import Optional, Union
from discord.ext import commands


class Confirm(discord.ui.View):
    def __init__(self, context: commands.Context, timeout: Optional[int] = 300, user: Optional[Union[discord.Member, discord.User]] = None):
        super().__init__(timeout=timeout)
        self.value = None
        self.context = context
        self.user = user or self.context.author

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def yes(self, b, i):
        if i.user != self.user:
            return await i.response.send_message("You cannot interact in other's commands.", ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label='No', style=discord.ButtonStyle.red)
    async def no(self, b, i):
        if i.user != self.user:
            return await i.response.send_message("You cannot interact in other's commands.", ephemeral=True)
        self.value = False
        self.stop()


class Paginator(discord.ui.View):
    def __init__(self, ctx, embeds):
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
        thread = await channel.start_thread(name=f'ticket-{interaction.user.id}')
        await thread.send(f"📂 {interaction.user.mention} has created a ticket.", allowed_mentions=discord.AllowedMentions(
            everyone=False,
            roles=False,
            users=True,
            replied_user=False
        ))

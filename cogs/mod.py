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

from utils.ui import Confirm
import discord
import asyncio

from discord.ext import commands
from discord.utils import escape_markdown
from humanfriendly import format_timespan
from typing import Union
from utils.bot import EpicBot
from utils.message import wait_for_msg
from utils.time import convert
from utils.random import gen_random_string
from utils.embed import success_embed, error_embed
from config import (
    BADGE_EMOJIS, EMOJIS, RED_COLOR
)

# warning: the code down below is absolute trash
# i can improve this by a lot, but i just dont have the time for that
# but im sure u do ;)


class AntiAltsSelectionView(discord.ui.View):
    def __init__(self, context):
        super().__init__(timeout=None)
        self.level = 0
        self.context = context
        self.cancelled = False

    @discord.ui.select(placeholder="Please select a level.", options=[
        discord.SelectOption(
            label="Level 01",
            description="Restrict the suspect from sending messages.",
            value='1',
            emoji='🔹'
        ),
        discord.SelectOption(
            label="Level 02",
            description="Kick the suspect from the server.",
            value='2',
            emoji='💎'
        ),
        discord.SelectOption(
            label="Level 03",
            description="Ban the suspect from the server.",
            value='3',
            emoji='<a:diamond:862594390256910367>'
        ),
    ])
    async def callback(self, select: discord.ui.Select, interaction: discord.Interaction):
        if interaction.user != self.context.author:
            return await interaction.response.send_message("You cannot interact in someone else's interaction.", ephemeral=True)
        self.level = int(select.values[0])
        await interaction.response.send_message(f"Alt protection Level **{select.values[0]}** has been selected. Please click the `Next` button to continue.", ephemeral=True)

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(self, b: discord.ui.Button, i: discord.Interaction):
        if i.user != self.context.author:
            return await i.response.send_message("You cannot interact in someone else's interaction.", ephemeral=True)
        self.cancelled = True
        self.stop()

    @discord.ui.button(label='Next', style=discord.ButtonStyle.green)
    async def next(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.context.author:
            return await interaction.response.send_message("You cannot interact in someone else's interaction.", ephemeral=True)
        if self.level == 0:
            return await interaction.response.send_message("Please select a level first!", ephemeral=True)
        self.stop()


class mod(commands.Cog, description="Keep your server safe! 🛠️"):
    def __init__(self, client: EpicBot):
        self.client = client

    @commands.command(help="Configure EpicBot antialts system.", aliases=['antiraid', 'antialt'])
    @commands.cooldown(3, 30, commands.BucketType.user)
    @commands.bot_has_guild_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def antialts(self, ctx, config=None, setting: Union[discord.TextChannel, discord.Role, int, str] = None):
        # yes i know this is messy
        # and i dont care
        prefix = ctx.clean_prefix
        g = await self.client.get_guild_config(ctx.guild.id)
        aa = g['antialts']
        enabled = False if not aa else True

        info_embed = success_embed(
            f"{BADGE_EMOJIS['bot_mod']}  Alt protection",
            f"""
Alt protection is current **{'Enabled' if enabled else 'Disabled'}**.

**Level:** `{'0' if not enabled else aa['level']}`
**Log channel:** {'None' if not enabled else '<#'+str(aa['log_channel'])+'>'}
**Minimum account age:** {'None' if not enabled else format_timespan(aa['min_account_age']*24*60*60)}
**Restricted Role:** {'None' if not enabled else '<@&'+str(aa['restricted_role'])+'>'}
            """
        ).add_field(
            name="🔹  Level 01",
            value="The bot will restrict the suspect from sending messages in the server and log their info.",
            inline=True
        ).add_field(
            name="💎  Level 02",
            value="The bot will kick the suspect and log their info, they will be banned if they try to join again.",
            inline=True
        ).add_field(
            name="<a:diamond:862594390256910367>  Level 03",
            value="The bot will ban the suspect and log their info.",
            inline=True
        ).add_field(
            name="Commands:",
            value=f"""
- `{prefix}antialt enable/disable` - To enable/disable alt protection.
- `{prefix}antialt minage <time>` - To set the minimum age.
- `{prefix}antialt level <number>` - To change the protection level.
- `{prefix}antialt channel #channel` - To change the log channel.
- `{prefix}antialt role @role` - To change the restricted role.

- `{prefix}kickalts` - Kicks all the users with the restricted role.
- `{prefix}banalts` - Bans all the users with the restricted role.
- `{prefix}grantaccess` - Grants server access to a restricted user.
                """
        )

        if config is None:
            return await ctx.reply(embed=info_embed)

        if config.lower() == 'enable':
            if enabled:
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Already enabled.", "Alt protection is already enabled."))

            log_channel = None
            min_account_age = None
            restricted_role = None

            view = AntiAltsSelectionView(context=ctx)
            msg = await ctx.reply(f"""
**Antialts setup**

- {EMOJIS['idle']} Level.
- {EMOJIS['dnd']} Log channel.
- {EMOJIS['dnd']} Minimum account age.
- {EMOJIS['dnd']} Restricted role.

Please select a protection level.
                                """, view=view)

            await view.wait()

            if view.cancelled:
                return await msg.edit(
                    content="",
                    embed=discord.Embed(title=f"{EMOJIS['tick_no']} Cancelled", color=RED_COLOR),
                    view=None
                )
            await msg.edit(f"""
**Antialts setup**

- {EMOJIS['online']} Level: `{view.level}`
- {EMOJIS['idle']} Log channel.
- {EMOJIS['dnd']} Minimum account age.
- {EMOJIS['dnd']} Restricted role.

Please enter a log channel.
Type `create` to automatically create a channel.
Type `cancel` to cancel the command.
                            """, view=None)
            m = await wait_for_msg(ctx, 60, msg)
            if m == 'pain':
                return
            if m.content.lower() == 'create':
                overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    ctx.guild.me: discord.PermissionOverwrite(read_messages=True)
                }
                created_channel = await ctx.guild.create_text_channel('alt-logs', overwrites=overwrites)
                log_channel = created_channel.id
            else:
                try:
                    lul_channel = await commands.TextChannelConverter().convert(ctx=ctx, argument=m.content)
                    log_channel = lul_channel.id
                except commands.ChannelNotFound:
                    return await msg.reply(content="", embed=error_embed(
                        f"{EMOJIS['tick_no']} Not found!",
                        f"I wasn't able to find the channel {m.content}, please try again."
                    ), view=None)

            await msg.edit(f"""
**Antialts setup**

- {EMOJIS['online']} Level: `{view.level}`
- {EMOJIS['online']} Log channel: <#{log_channel}>
- {EMOJIS['idle']} Minimum account age.
- {EMOJIS['dnd']} Restricted role.

Please enter the minimum account age requirement (in days).
Type `none` to have the default value (7 days).
Type `cancel` to cancel the setup.
                        """, view=None)

            m = await wait_for_msg(ctx, 60, msg)
            if m == 'pain':
                return
            try:
                if m.content.lower() != 'none':
                    temp_acc_age = int(m.content)
                    if temp_acc_age <= 0:
                        return await msg.edit(content="", embed=error_embed(
                            f"{EMOJIS['tick_no']} Positive values only!",
                            "Account age can only be a positive number."
                        ))
                    min_account_age = temp_acc_age
                else:
                    min_account_age = 7
            except Exception:
                return await msg.edit(content="", embed=error_embed(
                    f"{EMOJIS['tick_no']} Integer values only!",
                    "Please enter an integer next time."
                ))

            await msg.edit(f"""
**Antialts setup**

- {EMOJIS['online']} Level: `{view.level}`
- {EMOJIS['online']} Log channel: <#{log_channel}>
- {EMOJIS['online']} Minimum account age: {min_account_age} days.
- {EMOJIS['idle']} Restricted role.

Please enter a restricted role.
Type `create` to create one automatically.
Type `cancel` to cancel the setup.
                            """)

            m = await wait_for_msg(ctx, 60, msg)
            if m == 'pain':
                return
            if m.content.lower() != 'create':
                try:
                    r_role = await commands.RoleConverter().convert(ctx=ctx, argument=m.content)
                except Exception:
                    return await msg.edit(content="", embed=error_embed(
                        f"{EMOJIS['tick_no']} Not found!",
                        f"I wasn't able to find the role {m.content}\nPlease re-run the command."
                    ))
                restricted_role = r_role.id
            else:
                await msg.edit(f"Creating the role, this may take a while... {EMOJIS['loading']}")
                r_role = await ctx.guild.create_role(name="Restricted", color=0x818386)

                for channel in ctx.guild.channels:
                    try:
                        await channel.set_permissions(
                            r_role,
                            speak=False,
                            send_messages=False,
                            add_reactions=False
                        )
                    except Exception as e:
                        print(e)

                restricted_role = r_role.id

            await msg.edit(f"""
**Setup complete**

Here are you settings:

- {EMOJIS['online']} Level: `{view.level}`
- {EMOJIS['online']} Log channel: <#{log_channel}>
- {EMOJIS['online']} Minimum account age: {min_account_age} days.
- {EMOJIS['online']} Restricted role: <@&{restricted_role}>
                            """)

            g.update({"antialts": {
                "level": int(view.level),
                "log_channel": log_channel,
                "min_account_age": min_account_age,
                "restricted_role": restricted_role
            }})
            return

        if config.lower() == 'disable':
            if not enabled:
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Already disabled.", "Alt protection is already disabled."))
            g.update({"antialts": False})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Disabled",
                "Alt protection has now been disabled."
            ))

        if config.lower() == 'minage':
            if not enabled:
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Not enabled.", f"Please enable alt protection system first.\nUsage: `{prefix}antialts enable`"))
            if config is None:
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Invalid Usage", f"Please use `{prefix}antialts minage <number>`"))
            if not isinstance(setting, int):
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Intergers only!", "The minimum age number should be an integer only!"))
            if setting <= 0:
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Positive integers only!", "The minimum account age number can only be positive."))
            aa.update({"min_account_age": setting})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Updated!",
                f"The minimum account age has been updated to `{setting}` day(s)."
            ))

        if config.lower() == 'level':
            if not enabled:
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Not enabled.", f"Please enable alt protection system first.\nUsage: `{prefix}antialts enable`"))
            if config is None:
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Invalid Usage", f"Please use `{prefix}antialts level <number>`"))
            if not isinstance(setting, int):
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Intergers only!", "The level number should be an integer between 1 and 3 only!"))
            if not 1 <= setting <= 3:
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Invalid level value!", "The level number should be between and 1 and 3 only!"))
            aa.update({"level": setting})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Updated!",
                f"The alt protection level has been updated to level `{setting}`"
            ))

        if config.lower() == 'channel':
            if not enabled:
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Not enabled.", f"Please enable alt protection system first.\nUsage: `{prefix}antialts enable`"))
            if config is None:
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Invalid Usage", f"Please use `{prefix}antialts channel #channel`"))
            if not isinstance(setting, discord.TextChannel):
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Not found!", f"I wasn't able to find channel {setting}, please try again."))
            aa.update({"log_channel": setting.id})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Updated!",
                f"The log channel has been updated to {setting.mention}"
            ))

        if config.lower() == 'role':
            if not enabled:
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Not enabled.", f"Please enable alt protection system first.\nUsage: `{prefix}antialts enable`"))
            if config is None:
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Invalid Usage", f"Please use `{prefix}antialts role @role`"))
            if not isinstance(setting, discord.Role):
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Not found!", f"I wasn't able to find the role {setting}, please try again."))
            aa.update({"restricted_role": setting.id})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Updated!",
                f"The restricted role has been updated to {setting.mention}"
            ))

        else:
            return await ctx.reply(embed=info_embed)

    @commands.command(help="Kick all resitricted users by alt protection system.", aliases=['kickrestricted'])
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def kickalts(self, ctx: commands.Context):
        prefix = ctx.clean_prefix
        g = await self.client.get_guild_config(ctx.guild.id)
        aa = g['antialts']
        enabled = False if not aa else True
        if not enabled:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Alt protection not enabled!",
                f"You can only use this command if alt protection is enabled.\nPlease use `{prefix}antialts enable` to enable it."
            ))

        role = ctx.guild.get_role(aa['restricted_role'])
        if role is None:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Restricted role not found!",
                "Looks like the restricted role has been deleted."
            ))

        m = await ctx.reply(f"Working on it... {EMOJIS['loading']}")

        kids = role.members
        if len(kids) == 0:
            return await m.edit(content="", embed=error_embed(
                f"{EMOJIS['tick_no']} No restricted users found!",
                f"There are no users having the role {role.mention} in this server."
            ))
        kicked_count = 0
        for kid in kids:
            try:
                await kid.kick(reason=f"Action done by user: {ctx.author} ({ctx.author.id})")
                kicked_count += 1
                await asyncio.sleep(0.5)
            except Exception:
                pass
        await m.edit(f"I have kicked `{kicked_count}` restricted users out of `{len(kids)}`.")
        log_channel = self.client.get_channel(aa['log_channel'])
        if log_channel is None:
            return
        await log_channel.send(embed=success_embed(
            "Alts kicked!",
            f"**{kicked_count}** alts have been kicked by {ctx.author.mention}"
        ).set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url
        ).set_footer(text=f"ID: {ctx.author.id}"))

    @commands.command(help="Ban all resitricted users by alt protection system.", aliases=['banrestricted'])
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def banalts(self, ctx: commands.Context):
        prefix = ctx.clean_prefix
        g = await self.client.get_guild_config(ctx.guild.id)
        aa = g['antialts']
        enabled = False if not aa else True
        if not enabled:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Alt protection not enabled!",
                f"You can only use this command if alt protection is enabled.\nPlease use `{prefix}antialts enable` to enable it."
            ))

        role = ctx.guild.get_role(aa['restricted_role'])
        if role is None:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Restricted role not found!",
                "Looks like the restricted role has been deleted."
            ))

        m = await ctx.reply(f"Working on it... {EMOJIS['loading']}")

        kids = role.members
        if len(kids) == 0:
            return await m.edit(content="", embed=error_embed(
                f"{EMOJIS['tick_no']} No restricted users found!",
                f"There are no users having the role {role.mention} in this server."
            ))
        banned_count = 0
        for kid in kids:
            try:
                await kid.ban(reason=f"Action done by user: {ctx.author} ({ctx.author.id})")
                banned_count += 1
                await asyncio.sleep(0.5)
            except Exception:
                pass
        await m.edit(f"I have banned `{banned_count}` restricted users out of `{len(kids)}`.")
        log_channel = self.client.get_channel(aa['log_channel'])
        if log_channel is None:
            return
        await log_channel.send(embed=success_embed(
            "Alts banned!",
            f"**{banned_count}** alts have been banned by {ctx.author.mention}"
        ).set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url
        ).set_footer(text=f"ID: {ctx.author.id}"))

    @commands.command(help="Give server access to a user who is restricted.", aliases=['giveaccess', 'unrestrict'])
    @commands.cooldown(3, 30, commands.BucketType.user)
    @commands.bot_has_guild_permissions(manage_roles=True, ban_members=True)
    @commands.has_permissions(manage_roles=True)
    async def grantaccess(self, ctx, user: Union[discord.Member, discord.User, str] = None):
        prefix = ctx.clean_prefix
        g = await self.client.get_guild_config(ctx.guild.id)
        aa = g['antialts']
        enabled = False if not aa else True
        if not enabled:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Not enabled!",
                "You need to enable alt protection in order to use this command."
            ))
        role = ctx.guild.get_role(aa['restricted_role'])
        if user is None:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Please mention a user.",
                f"Correct usage: `{prefix}grantaccess @user/userid`"
            ))
        if isinstance(user, discord.Member):
            if role not in user.roles:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Access already granted!",
                    "It looks like this user already has access to the server."
                ))
            await user.remove_roles(role, reason=f"Access granted by {ctx.author} ({ctx.author.id})")
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Access granted!",
                f"Access to the server has been granted to the user {user.mention}"
            ))
        elif isinstance(user, discord.User):
            bans = await ctx.guild.bans()
            for b in bans:
                if b.user == user:
                    await ctx.guild.unban(b.user, f"Access granted by {ctx.author} ({ctx.author.id})")
                    return await ctx.reply(embed=success_embed(
                        f"{EMOJIS['tick_yes']} Access granted!",
                        f"Access to the server has been granted to the user {user.mention}"
                    ))
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Access already granted!",
                "It looks like this user already has access to the server."
            ))
        raise commands.UserNotFound(user)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True, manage_channels=True)
    @commands.command(help="Mute someone.")
    async def mute(self, ctx: commands.Context, user: discord.Member = None, *, reason="No Reason Provided"):
        prefix = ctx.clean_prefix
        if user is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please mention a user.\nCorrect Usage: `{prefix}mute @user [reason]`\nExample: `{prefix}mute @egirl spamming`"
            ))
        if user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Bruh!", "You can't mute yourself!"))
        if user == self.client.user:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(":(", "Why u do this to me?! *cries*"))
        if user.bot:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Bruh!", "You can't mute bots!"))
        if int(user.top_role.position) >= int(ctx.author.top_role.position) and ctx.author.id != ctx.guild.owner_id:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} No!",
                f"You cannot mute **{escape_markdown(str(user))}** because they are a mod/admin."
            ))
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role is None:
            muted_role = await ctx.guild.create_role(name="Muted", color=0x818386)

            for channel in ctx.guild.channels:
                try:
                    await channel.set_permissions(
                        muted_role,
                        speak=False,
                        send_messages=False,
                        add_reactions=False
                    )
                except Exception as e:
                    print(e)
        try:
            if muted_role in user.roles:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Bruh!", f"**{escape_markdown(str(user))}** is already muted!"))
            await user.add_roles(muted_role, reason=f"{ctx.author} ({ctx.author.id}): {reason}")
        except Exception:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Missing Permissions!",
                f"The {muted_role.mention} role is higher than my top role.\nPlease give me a higher role to fix this issue."
            ))
        await ctx.reply(embed=success_embed(
            f"{EMOJIS['muted']} Done!",
            f"I have muted **{escape_markdown(str(user))}**."
        ))
        try:
            await user.send(embed=success_embed(
                f"{EMOJIS['muted']} You have been muted!",
                f"You were muted in **{escape_markdown(str(ctx.guild))}**."
            ).add_field(name="Reason:", value=reason, inline=False))
        except Exception:
            pass

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True, manage_channels=True)
    @commands.command(help="Unmute a muted user.")
    async def unmute(self, ctx: commands.Context, user: discord.Member = None):
        prefix = ctx.clean_prefix
        if user is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please mention a user.\nCorrect Usage: `{prefix}unmute @user [reason]`\nExample: `{prefix}unmute @egirl`"
            ))
        if user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Bruh!", "You can't unmute yourself!"))
        if user == self.client.user:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed("Bruh", "You can't use this command on me!"))
        if user.bot:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Bruh!", "You can't unmute bots!"))
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role is None:
            muted_role = await ctx.guild.create_role(name="Muted", color=0x818386)

            for channel in ctx.guild.channels:
                try:
                    await channel.set_permissions(
                        muted_role,
                        speak=False,
                        send_messages=False,
                        add_reactions=False
                    )
                except Exception as e:
                    print(e)
            return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Bruh!", f"**{escape_markdown(str(user))}** is not muted!"))
        try:
            if muted_role not in user.roles:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Bruh!", f"**{escape_markdown(str(user))}** is not muted!"))
            await user.remove_roles(muted_role, reason=f"Unmuted by: {ctx.author} ({ctx.author.id})")
        except Exception:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Missing Permissions!",
                f"The {muted_role.mention} role is higher than my top role.\nPlease give me a higher role to fix this issue."
            ))
        await ctx.reply(embed=success_embed(
            f"{EMOJIS['unmuted']} Done!",
            f"I have unmuted **{escape_markdown(str(user))}**."
        ))
        try:
            await user.send(embed=success_embed(
                f"{EMOJIS['unmuted']} You have been unmuted!",
                f"You were unmuted in **{escape_markdown(str(ctx.guild))}**."
            ))
        except Exception:
            pass

    @commands.cooldown(3, 30, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    @commands.bot_has_permissions(manage_channels=True, manage_roles=True)
    @commands.command(help="Lock a channel.")
    async def lock(self, ctx: commands.Context, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)}
            await channel.edit(overwrites=overwrites)
            await ctx.send(f"{EMOJIS['tick_yes']} {channel.mention} has now been locked.")

        elif channel.overwrites[ctx.guild.default_role].send_messages or channel.overwrites[ctx.guild.default_role].send_messages is None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"{EMOJIS['tick_yes']} {channel.mention} has now been locked.")
        else:
            await ctx.send(f"{EMOJIS['tick_no']} {channel.mention} is already locked ._.")

    @commands.command(help="Lock the whole server.")
    @commands.has_permissions(manage_guild=True, manage_channels=True, manage_roles=True)
    @commands.bot_has_permissions(manage_guild=True, manage_channels=True, manage_roles=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def lockdown(self, ctx: commands.Context):
        v = Confirm(ctx, 60)
        m = await ctx.reply("Are you sure you want to lock the whole server?", view=v)
        await v.wait()
        if not v.value:
            return
        await m.delete()
        async with ctx.typing():
            i = 0
            for channel in ctx.guild.channels:
                if isinstance(channel, discord.TextChannel):
                    await ctx.invoke(self.client.get_command('lock'), channel=channel)
                    await asyncio.sleep(0.5)
                    i += 1
            await ctx.send(f"**{EMOJIS['tick_yes']} {i} channels have been locked.**")

    @commands.cooldown(3, 30, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    @commands.bot_has_permissions(manage_channels=True, manage_roles=True)
    @commands.command(help="Unlock a channel.")
    async def unlock(self, ctx: commands.Context, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        if not channel.overwrites[ctx.guild.default_role].send_messages:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f"{EMOJIS['tick_yes']} {channel.mention} has now been unlocked.")
        else:
            await ctx.send(f"{EMOJIS['tick_no']} {channel.mention} is already unlocked ._.")

    @commands.command(help="Lock the whole server.")
    @commands.has_permissions(manage_guild=True, manage_channels=True, manage_roles=True)
    @commands.bot_has_permissions(manage_guild=True, manage_channels=True, manage_roles=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def unlockdown(self, ctx: commands.Context):
        v = Confirm(ctx, 60)
        m = await ctx.reply("Are you sure you want to unlock the whole server?", view=v)
        await v.wait()
        if not v.value:
            return
        await m.delete()
        async with ctx.typing():
            i = 0
            for channel in ctx.guild.channels:
                if isinstance(channel, discord.TextChannel):
                    await ctx.invoke(self.client.get_command('unlock'), channel=channel)
                    await asyncio.sleep(0.5)
                    i += 1
            await ctx.send(f"**{EMOJIS['tick_yes']} {i} channels have been unlocked.**")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True, embed_links=True)
    @commands.command(help="Kick someone from your server!")
    async def kick(self, ctx: commands.Context, user: discord.Member = None, *, reason='No Reason Provided'):
        PREFIX = ctx.clean_prefix
        if user is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter a user to kick.\nCorrect Usage: `{PREFIX}kick @user [reason]`"
            ))
        if user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply("Don't kick yourself :(")
        if user == self.client.user:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply("Bruh why u wanna kick me :(")
        if int(user.top_role.position) >= int(ctx.author.top_role.position) and ctx.author.id != ctx.guild.owner_id:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} No!",
                f"You cannot kick **{escape_markdown(str(user))}** because they are a mod/admin."
            ))
        try:
            await user.kick(reason=f"{ctx.author} - {ctx.author.id}: {reason}")
            try:
                await user.send(embed=discord.Embed(
                    title="You have been kicked!",
                    description=f"You were kicked from the server: **{ctx.guild}**",
                    color=RED_COLOR
                ).add_field(name="Moderator", value=f" {ctx.author.mention} - {escape_markdown(str(ctx.author))}", inline=False
                ).add_field(name="Reason", value=reason, inline=False))
            except Exception:
                pass
            await ctx.message.reply(embed=success_embed(f"{EMOJIS['tick_yes']} User Kicked!", f"**{escape_markdown(str(user))}** has been kicked!"))
        except Exception:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed("Error!", f"I cannot kick **{escape_markdown(str(user))}** because they are a mod/admin."))

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True, embed_links=True)
    @commands.command(help="Ban multiple people from your server!")
    async def massban(self, ctx: commands.Context, users: commands.Greedy[Union[discord.Member, discord.User, int, str]] = None, *, reason='No Reason Provided'):
        if not users:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("Please provide some users to ban!")
        for user in users:
            await ctx.invoke(self.client.get_command('ban'), user=user, reason=reason)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(ban_members=True, embed_links=True)
    @commands.command(help="Kick multiple people from your server!")
    async def masskick(self, ctx: commands.Context, users: commands.Greedy[discord.Member] = None, *, reason='No Reason Provided'):
        if not users:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("Please provide some users to kick!")
        for user in users:
            await ctx.invoke(self.client.get_command('kick'), user=user, reason=reason)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True, embed_links=True)
    @commands.command(help="Ban someone from your server!", aliases=['hackban'])
    async def ban(self, ctx: commands.Context, user: Union[discord.Member, discord.User, int, str] = None, *, reason="No Reason Provided"):
        PREFIX = ctx.clean_prefix
        if user is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter a user to ban.\nCorrect Usage: `{PREFIX}ban @user [reason]`"
            ))
        if isinstance(user, str):
            raise commands.UserNotFound(user)
        if isinstance(user, int):
            try:
                await ctx.guild.ban(discord.Object(id=user), reason=f"{ctx.author} - {ctx.author.id}: {reason}")
                await ctx.send(embed=success_embed(f"{EMOJIS['tick_yes']}", "They have been banned."))
            except Exception as e:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=error_embed(f"{EMOJIS['tick_no']} Unable to ban", e))
        if user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("Don't ban yourself :(")
        if user == self.client.user:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("Bruh why u wanna ban me :(")
        if isinstance(user, discord.Member):
            if int(user.top_role.position) >= int(ctx.author.top_role.position) and ctx.author.id != ctx.guild.owner_id:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=error_embed(
                    f"{EMOJIS['tick_no']} No!",
                    f"You cannot ban **{escape_markdown(str(user))}** because they are a mod/admin."
                ))
        try:
            await ctx.guild.ban(user, reason=f"{ctx.author} - {ctx.author.id}: {reason}")
            try:
                await user.send(embed=discord.Embed(
                    title="You have been banned!",
                    description=f"You were banned from the server: **{ctx.guild}**",
                    color=RED_COLOR
                ).add_field(name="Moderator", value=f"{ctx.author.mention} - {escape_markdown(str(ctx.author))}", inline=False
                ).add_field(name="Reason", value=reason, inline=False))
            except Exception:
                pass
            await ctx.send(embed=success_embed(f"{EMOJIS['tick_yes']} User Banned!", f"**{escape_markdown(str(user))}** has been banned!"))
        except Exception:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=error_embed("Error!", f"I cannot ban **{escape_markdown(str(user))}** because they are a mod/admin."))

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True, embed_links=True)
    @commands.command(help="Unban a user from your server.")
    async def unban(self, ctx: commands.Context, *, user=None):
        PREFIX = ctx.clean_prefix
        if user is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage",
                f"Please enter a member to unban.\nCorrect Usage: `{PREFIX}unban <user>`\nExample: `{PREFIX}unban egirl#1234`"
            ))
        banned_users = await ctx.guild.bans()
        try:
            user_id = int(user)
        except Exception:
            user_id = None
        if user_id is not None:
            for ban_entry in banned_users:
                user_uwu = ban_entry.user
                if user_id == user_uwu.id:
                    await ctx.guild.unban(user_uwu, reason=f"Command used by: {ctx.author} ({ctx.author.id})")
                    return await ctx.message.reply(embed=success_embed(
                        f"{EMOJIS['tick_yes']} Member Unbanned!",
                        f"**{escape_markdown(str(user_uwu))}** has been unbanned."
                    ))
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Not found!",
                f"Either member with ID: **{user_id}** doesn't exist OR they are not banned."
            ))
        elif user_id is None:
            if '#' not in user:
                ctx.command.reset_cooldown(ctx)
                return await ctx.message.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Usage",
                    "Please provide a proper user to unban.\nExample of a proper user: `abcd#1234`"
                ))
            member_name, member_discriminator = user.split('#')

            for ban_entry in banned_users:
                user_uwu = ban_entry.user
                print(user_uwu)
                print(user)

                if (user_uwu.name, user_uwu.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user_uwu, reason=f"Command used by: {ctx.author} ({ctx.author.id})")
                    return await ctx.message.reply(embed=success_embed(
                        f"{EMOJIS['tick_yes']} Member Unbanned!",
                        f"**{escape_markdown(str(user_uwu))}** hass been unbanned."
                    ))
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Not found!",
                f"User **{escape_markdown(str(user))}** doesn't exist OR they aren't banned."
            ))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True, embed_links=True)
    @commands.command(aliases=['clear'], help="Purge a channel.")
    async def purge(self, ctx: commands.Context, amount='10', user: discord.Member = None):
        PREFIX = ctx.clean_prefix
        try:
            amount = int(amount)
        except Exception:
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter an integer as the amount.\n\nCorrect Usage: `{PREFIX}purge <amount>` OR `{PREFIX}purge <amount> @user`\nExample: `{PREFIX}purge 10` OR `{PREFIX}purge 10 @egirl`"
            ))
        if amount > 500:
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Error!",
                "The amount cannot be greater than **500**"
            ))
        if user is None:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=(amount))
            uwu = []
            owo = []

            for msg in deleted:
                uwu.append(msg.author.id)
                if msg.author.id not in owo:
                    owo.append(msg.author.id)

            hee = ""

            for e in owo:
                hee += f"<@{e}> - **{uwu.count(e)}** messages\n"

            return await ctx.send(embed=success_embed(
                f"{EMOJIS['tick_yes']} Channel Purged!",
                f"**{amount+1}** message(s) deleted!\n\n{hee}"
            ), delete_after=5)
        elif user is not None:
            def check(e):
                return e.author == user
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount, check=check)
            return await ctx.send(embed=success_embed(
                f"{EMOJIS['tick_yes']} Channel Purged!",
                f"**{amount}** message(s) deleted from {user.mention}"
            ), delete_after=5)

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.command(help="Change the slowmode of a channel.")
    async def slowmode(self, ctx: commands.Context, amount=None):
        PREFIX = ctx.clean_prefix
        if amount is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter an amount.\nCorrect Usage: `{PREFIX}slowmode <amount>`\nExample: `{PREFIX}slowmode 5s`"
            ))
        try:
            amount = int(amount)
            if amount < 0:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Usage!",
                    "The slowmode value can't be negative."
                ))
            converted_time = [amount, amount, 'second(s)']
        except Exception:
            converted_time = convert(amount)
            if converted_time == -1:
                ctx.command.reset_cooldown(ctx)
                return await ctx.message.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Usage!",
                    f"Please enter a proper unit of time (s/m/h/d).\nExample: `{PREFIX}slowmode 10s` OR `{PREFIX}slowmode 1h`"
                ))
            if converted_time == -2:
                ctx.command.reset_cooldown(ctx)
                return await ctx.message.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Usage!",
                    f"Please enter a proper integer for time.\nExample: `{PREFIX}slowmode 10s`"
                ))
            if converted_time == -3:
                ctx.command.reset_cooldown(ctx)
                return await ctx.message.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Usage!",
                    f"Please enter a positive value of time next time.\nExample: `{PREFIX}slowmode 10s`"
                ))
        if converted_time[0] > 21600:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Too high!",
                "The maximum slowmode can only be **6 hours** (21600 seconds)."
            ))
        await ctx.channel.edit(slowmode_delay=converted_time[0])
        await ctx.message.reply(embed=success_embed(
            f"{EMOJIS['tick_yes']} Slowmode Changed!",
            f"The slowmode has now been set to **{converted_time[1]} {converted_time[2]}**"
        ))

    @commands.cooldown(2, 15, commands.BucketType.user)
    @commands.has_guild_permissions(kick_members=True)
    @commands.command(help="Warn a user.")
    async def warn(self, ctx: commands.Context, user: discord.Member = None, *, reason='No Reason Provided'):
        custom_prefix = ctx.clean_prefix
        if user is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please mention a user next time.\nExample: `{custom_prefix}warn @egirl spamming`"
            ))
        if user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Bruh!",
                "You cannot warn yourself."
            ))
        if user == self.client.user:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Bruh!",
                "You cannot warn me."
            ))
        if user.bot:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Bruh!",
                "You cannot warn bots."
            ))
        if int(ctx.author.top_role.position) <= int(user.top_role.position):
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Error!",
                "You cannot warn a mod/admin."
            ))
        if len(reason) > 500:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Too long!",
                "The reason provided was too long, please try again."
            ))
        random_generated_id = gen_random_string(20)
        await self.client.warnings.insert_one({
            "_id": random_generated_id,
            "user_id": user.id,
            "guild_id": ctx.guild.id,
            "moderator": ctx.author.id,
            "reason": reason
        })
        try:
            await user.send(embed=error_embed(
                "You have been warned!",
                f"You were warned from the server: **{escape_markdown(str(ctx.guild))}**"
            ).add_field(name="Moderator:", value=f"{ctx.author.mention} - {escape_markdown(str(ctx.author))}", inline=False
            ).add_field(name="Reason:", value=reason, inline=False
            ).set_footer(text=f"Warn ID: {random_generated_id}"))
        except Exception as e:
            print(e)
        await ctx.message.reply(embed=success_embed(
            f"{EMOJIS['tick_yes']} User Warned!",
            f"**{escape_markdown(str(user))}** has been warned!"
        ).set_footer(text=f"Warn ID: {random_generated_id}"))

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.has_guild_permissions(kick_members=True)
    @commands.command(aliases=['removewarn', 'deletewarn', 'removewarning', 'deletewarning', 'delwarning'], help="Delete a warning.")
    async def delwarn(self, ctx: commands.Context, warn_id=None):
        prefix = ctx.clean_prefix
        if warn_id is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter a warn ID.\nExample: `{prefix}delwarn N3vE4g0nN4g1V3y0UUp`"
            ))
        ah_yes = await self.client.warnings.find_one({
            "_id": warn_id,
            "guild_id": ctx.guild.id
        })
        if ah_yes is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Not found!",
                "The provided warning ID is Invalid.\nPlease enter a valid warning ID."
            ))
        await self.client.warnings.delete_one({"_id": warn_id})
        return await ctx.message.reply(embed=success_embed(
            f"{EMOJIS['tick_yes']} Warning Removed!",
            f"The warning: `{warn_id}` was deleted!"
        ).add_field(
            name="Some info on the warning:",
            value=f"""
```yaml
User Warned: {self.client.get_user(ah_yes['user_id'])}
Moderator: {self.client.get_user(ah_yes['moderator'])}
Reason: {ah_yes['reason']}
```
            """,
            inline=False
        ))

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.has_guild_permissions(kick_members=True)
    @commands.command(aliases=['warnings'], help="Check warnings of a user!")
    async def warns(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        ah_yes = self.client.warnings.find({
            "user_id": user.id,
            "guild_id": ctx.guild.id
        })
        uwu = await ah_yes.to_list(length=None)
        if len(uwu) == 0:
            return await ctx.message.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Warnings!",
                f"**{escape_markdown(str(user))}** has no warnings."
            ))
        uwu_embed = success_embed(
            f"{EMOJIS['tick_yes']} Warnings",
            f"Warnings of **{escape_markdown(str(user))}**."
        )
        if len(uwu) <= 25:
            for e in uwu:
                uwu_embed.add_field(
                    name=f"Warning ID: `{e['_id']}`",
                    value=f"""
```yaml
Moderator: {self.client.get_user(e['moderator'])}
Reason: {e['reason']}
```
                    """,
                    inline=False
                )
        if len(uwu) > 25:
            i = 0
            for e in uwu:
                if i == 25:
                    break
                uwu_embed.add_field(
                    name=f"Warning ID: `{e['_id']}`",
                    value=f"""
```yaml
Moderator: {self.client.get_user(e['moderator'])}
Reason: {e['reason']}
```
                    """,
                    inline=False
                )
                i += 1
        return await ctx.message.reply(embed=uwu_embed)


def setup(client):
    client.add_cog(mod(client))

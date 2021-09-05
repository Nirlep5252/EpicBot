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
import asyncio
import json
import typing as t

from discord.ext import commands, tasks
from config import (
    EMOJIS, WEBSITE_LINK, SUPPORT_SERVER_LINK,
    MAIN_COLOR, DISABLE, PREMIUM_GUILDS,
    RED_COLOR, ENABLE, custom_cmds_tags_lemao,
    DEFAULT_WELCOME_MSG, DEFAULT_LEAVE_MSG,
    DEFAULT_AUTOMOD_CONFIG, GLOBAL_CHAT_RULES,
    DEFAULT_LEVEL_UP_MSG, BADGE_EMOJIS, ANTIHOIST_CHARS,
    EMOJIS_FOR_COGS
)
from utils.embed import error_embed, success_embed, process_embeds_from_json
from utils.bot import EpicBot
from utils.ui import Confirm, Paginator, SelfRoleEditor, SelfRoleOptionSelecter, TicketView
from utils.converters import AddRemoveConverter, Category, Lower
from utils.message import wait_for_msg
from utils.recursive_utils import prepare_emojis_and_roles
from utils.reactions import prepare_rolemenu

autoposting_delay = 300


class config(commands.Cog, description="Configure your server with amazing EpicBot modules"):
    def __init__(self, client: EpicBot):
        self.client = client
        self.sfw_posting_modules = {
            'meme': 'https://meme-api.herokuapp.com/gimme',
            'waifu': 'https://shiro.gg/api/images/neko',
            'wallpapers': 'https://shiro.gg/api/images/wallpapers',
            'pikachu': 'https://some-random-api.ml/img/pikachu',
            'cat': 'https://some-random-api.ml/img/cat',
            'dog': 'https://some-random-api.ml/img/dog',
            'fox': 'https://some-random-api.ml/img/fox',
            'panda': 'https://some-random-api.ml/img/panda',
            'redpanda': 'https://some-random-api.ml/img/red_panda'
        }
        self.nsfw_posting_modules = {
            'hentai': 'https://nekos.life/api/v2/img/hentai',
            'thighs': 'https://shiro.gg/api/images/nsfw/thighs',
            'boobs': 'https://nekos.life/api/v2/img/boobs',
            'pussy': 'https://nekos.life/api/v2/img/pussy',
            'blowjob': 'https://nekos.life/api/v2/img/blowjob',
            'nekogif': 'https://nekos.life/api/v2/img/nsfw_neko_gif',
            'cum': 'https://nekos.life/api/v2/img/cum',
            'spank': 'https://nekos.life/api/v2/img/spank',
            'anal': 'https://nekos.life/api/v2/img/anal',
            'trap': 'https://nekos.life/api/v2/img/trap'
        }
        self.good_commands = [
            'blacklist', 'unblacklist', 'dm',
            'help', 'ping', 'invite', 'vote', 'support',
            'credits', 'uptime', 'privacy', 'bugreport',
            'disable', 'enable', 'disabled_list', 'prefix',
            'autopost', 'customcommand', 'customlist', 'disablecategory',
            'enablecategory'
        ]
        self.actual_autoposting_lmao.start()

    async def get_image_from_api_sex(self, url):
        try:
            async with self.client.session.get(url) as r:
                try:
                    uwu = await r.json()
                    try:
                        image = uwu['url']
                        return image
                    except KeyError:
                        image = uwu['link']
                        return image
                    except Exception as e:
                        print(f"Error in getting image in autoposting: {e}")
                        return 'pain'
                except Exception as e:
                    print(f"Unable to convert json response for {url}: {e}")
                    return 'pain'
        except Exception as e:
            print(f"ERROR in getting image for {url} in autoposting: {e}")
            return 'pain'

    async def get_webhook_autopost(self, channel_id: int) -> discord.Webhook:
        channel = self.client.get_channel(channel_id)
        if not channel:
            return False
        try:
            webhooks = await channel.webhooks()
        except Exception:
            return False
        webhook = discord.utils.get(webhooks, name="EpicBot Autoposting", user=self.client.user)
        if not webhook:
            try:
                webhook = await channel.create_webhook(
                    name="EpicBot Autoposting",
                    reason="EpicBot Autoposting!"
                )
            except Exception:
                return False
        return webhook

    async def send_from_webhook_autopost(self, webhook, embed):
        await webhook.send(
            embed=embed,
            avatar_url=self.client.user.display_avatar.url
        )

    @tasks.loop(seconds=autoposting_delay)
    async def actual_autoposting_lmao(self):
        image_cache = {}

        for e in self.client.serverconfig_cache:
            for ee in e['autoposting']:
                channel = self.client.get_channel(ee['channel_id'])
                if channel is not None:
                    webhook = await self.get_webhook_autopost(channel.id)
                    if ee['nsfw'] and not channel.is_nsfw():
                        try:
                            embed = error_embed(
                                f"{EMOJIS['tick_no']} Autoposting Error!",
                                f"Please mark this channel as **NSFW** for `{ee['name']}` autoposting to work."
                            )
                            if webhook:
                                await self.send_from_webhook_autopost(webhook, embed)
                            else:
                                await channel.send(embed=embed)
                        except Exception as e:
                            print(f"Failed autoposting in channel: #{channel.name} ({channel.id}) in guild {channel.guild} ({channel.guild.id}). ERROR: {e}")

                    HMMMM = self.nsfw_posting_modules if ee['nsfw'] else self.sfw_posting_modules

                    if ee['name'] in image_cache:
                        image_url = image_cache[ee['name']]
                    else:
                        image_url = await self.get_image_from_api_sex(HMMMM[ee['name']])
                        image_cache.update({ee['name']: image_url})
                    owo_embed = error_embed(
                        "An error occured while autoposting.",
                        "The error has been automatically reported to the devs and will be fixed soon."
                    )
                    uwu_embed = success_embed(
                        f"{ee['name'].title()} Autoposting!",
                        f"[Invite EpicBot]({WEBSITE_LINK}/invite) | [Vote EpicBot]({WEBSITE_LINK}/vote) | [Support Server]({SUPPORT_SERVER_LINK})"
                    ).set_footer(text=f"Posting every {autoposting_delay} seconds!")
                    if image_url != 'pain':
                        uwu_embed.set_image(url=image_url)
                    try:
                        if ee['nsfw'] and channel.is_nsfw() or not ee['nsfw']:
                            if webhook:
                                await self.send_from_webhook_autopost(webhook, owo_embed if image_url == 'pain' else uwu_embed)
                            else:
                                await channel.send(embed=owo_embed if image_url == 'pain' else uwu_embed)
                            await asyncio.sleep(1)
                    except Exception as e:
                        print(f"Failed autoposting in channel: #{channel.name} ({channel.id}) in guild {channel.guild} ({channel.guild.id}). ERROR: {e}")

    async def check_if_autopost_module_is_enabled_or_not(self, guild_config_ap, module):
        for e in guild_config_ap:
            if e['name'] == module.lower():
                return e
        return False

    @commands.command(help="Configure self roles for members in your server!", aliases=['selfrole', 'reactionrole', 'rr', 'rrole', 'reactionroles', 'rolemenu'])
    @commands.has_permissions(manage_guild=True, manage_roles=True)
    @commands.bot_has_permissions(administrator=True)
    @commands.cooldown(3, 120, commands.BucketType.guild)
    @commands.max_concurrency(3, commands.BucketType.guild)
    async def selfroles(self, ctx: commands.Context, option: Lower = None, message_id: t.Optional[int] = None):
        async with ctx.typing():
            prefix = ctx.clean_prefix
            guild_self_roles = await self.client.self_roles.find_one({"_id": ctx.guild.id})
            if guild_self_roles is None:
                await self.client.self_roles.insert_one({
                    "_id": ctx.guild.id,
                    "role_menus": {}
                })
                guild_self_roles = await self.client.self_roles.find_one({"_id": ctx.guild.id})
            role_menus = guild_self_roles['role_menus']
            info_embed = success_embed(
                f"{EMOJIS['reaction']} Self Roles",
                f"""
The server currently has **{len(role_menus)}** role menu{'s' if len(role_menus) != 1 else ''}.

**You can use the following commands to configure role menus:**

- `{prefix}selfrole create` - Creates a new rolemenu.
- `{prefix}selfrole edit` - Edits an existing rolemenu.
- `{prefix}selfrole delete` - Deletes an existing rolemenu.
- `{prefix}selfrole list` - Shows all the current rolemenus.
                """
            )
            if not option:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=info_embed)
            if option in ['create', 'new']:
                if len(role_menus) >= 20:
                    return await ctx.reply("You can only have max `20` rolemenus.")
                view = SelfRoleOptionSelecter(ctx)
                main_msg = await ctx.reply(embed=success_embed(
                    f"{EMOJIS['loading']} Rolemenu creation...",
                    "Please select a rolemenu type for this rolemenu!"
                ), view=view)
                await view.wait()
                if view.value is None:
                    ctx.command.reset_cooldown(ctx)
                    return await main_msg.edit(content=f"{EMOJIS['tick_no']}Command cancelled.", embed=None, view=None)
                self_role_type = view.value
                await main_msg.edit(embed=success_embed(
                    f"{EMOJIS['loading']} Rolemenu creation...",
                    "Please send the channel in which you want the rolemenu to be in."
                ), view=None)
                m = await wait_for_msg(ctx, 60, main_msg)
                if m == 'pain':
                    ctx.command.reset_cooldown(ctx)
                    return
                try:
                    text_channel = await commands.TextChannelConverter().convert(ctx, m.content)
                except Exception:
                    await main_msg.delete()
                    raise commands.ChannelNotFound(m.content)
                if self_role_type == 'reaction':
                    await main_msg.edit(embed=success_embed(
                        f"{EMOJIS['loading']} Rolemenu creation...",
                        "If you would like to have the rolemenu in an already sent message, please enter the message ID of that message.\n\nYou can send `none` to skip this step."
                    ))
                    m = await wait_for_msg(ctx, 60, main_msg)
                    if m == 'pain':
                        return
                    if m.content.lower() != 'none':
                        try:
                            custom_msg = await text_channel.fetch_message(int(m.content.lower()))
                            custom_msg_id = custom_msg.id
                        except Exception:
                            custom_msg_id = None
                            await ctx.send("I wasn't able to find the message from your message ID, so I will create a rolemenu message for you.")
                    else:
                        custom_msg_id = None
                else:
                    custom_msg_id = None
                await main_msg.edit(embed=success_embed(
                    f"{EMOJIS['loading']} Rolemenu creation...",
                    "Please send all the roles separated with a comma `,`.\n\nExample: `@Artist, @Foodie, @Music Lover, @Cutie`\nPlease follow this format."
                ))
                m = await wait_for_msg(ctx, 60, main_msg)
                if m == 'pain':
                    return
                roles_text_list = m.content.replace(" ", "").split(",")
                roles = []
                for role_text in roles_text_list:
                    try:
                        role = await commands.RoleConverter().convert(ctx, role_text)
                        if role.position < ctx.guild.me.top_role.position and (role.position < ctx.author.top_role.position or ctx.author == ctx.guild.owner) and role not in roles:
                            roles.append(role)
                    except Exception:
                        pass
                if len(roles) == 0:
                    ctx.command.reset_cooldown(ctx)
                    return await main_msg.edit(embed=error_embed(
                        f"{EMOJIS['tick_no']} Error!",
                        f"Looks like no roles were found in your message.\nOr all the roles were above my top role.\nYou can join our **[Support Server]({SUPPORT_SERVER_LINK})** for help."
                    ))
                await main_msg.edit(content="", embed=success_embed(
                    f"{len(roles)} Roles found!",
                    f"I have found **{len(roles)}** in your message.\n\n{' '.join(role.mention for role in roles)}\n\nNow you need to react to this message with the corresponding emojis for the rolemenu to be complete!"
                ), view=None)
                final_output = await prepare_emojis_and_roles(ctx, roles, main_msg)
                if final_output is None:
                    return
                msg_id = await prepare_rolemenu(ctx, final_output, text_channel, self_role_type, custom_msg_id)
                role_menus = guild_self_roles['role_menus']
                role_menus.update({
                    str(msg_id): {
                        "type": self_role_type,
                        "channel": text_channel.id,
                        "stuff": final_output
                    }
                })
                await self.client.self_roles.update_one(
                    filter={"_id": ctx.guild.id},
                    update={"$set": {"role_menus": role_menus}}
                )
                return await main_msg.edit(content=f"The rolemenu has been setup in {text_channel.mention}", embed=None, view=None)
            if option in ['delete', 'remove']:
                if message_id is None:
                    ctx.command.reset_cooldown(ctx)
                    return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Invalid Usage!", "Please mention a message ID."))
                if str(message_id) not in role_menus:
                    ctx.command.reset_cooldown(ctx)
                    return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Not found!", "This rolemenu doesn't exist."))
                role_menus.pop(str(message_id))
                await self.client.self_roles.update_one(
                    filter={"_id": ctx.guild.id},
                    update={"$set": {"role_menus": role_menus}}
                )
                return await ctx.reply(embed=success_embed(f"{EMOJIS['tick_yes']} Rolemenu removed!", "The rolemenu has been removed from the database, you can now delete the message."))
            if option in ['show', 'list']:
                embed = success_embed(
                    f"{EMOJIS['tick_yes']} Your rolemenus!",
                    f"This server has a total of **{len(role_menus)}** rolemenus."
                )
                for msg_id, menu in role_menus.items():
                    embed.add_field(
                        name=msg_id,
                        value=f"""
**Message:** [Click me](https://discord.com/channels/{ctx.guild.id}/{menu['channel']}/{msg_id})
**Menu type:** {menu['type'].title()}
**Roles:** {len(menu['stuff'])}
**Channel:** <#{menu['channel']}>
                        """,
                        inline=False
                    )
                return await ctx.reply(embed=embed)
            if option in ['edit']:
                if message_id is None:
                    ctx.command.reset_cooldown(ctx)
                    return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Invalid Usage!", "Please mention a message ID."))
                if str(message_id) not in role_menus:
                    ctx.command.reset_cooldown(ctx)
                    return await ctx.reply(embed=error_embed(f"{EMOJIS['tick_no']} Not found!", "This rolemenu doesn't exist."))
                view = SelfRoleEditor(ctx)
                main_msg = await ctx.reply(embed=success_embed(
                    f"{EMOJIS['loading']} What would you like to edit?",
                    "Please select an option!"
                ), view=view)
                await view.wait()
                if not view.value:
                    ctx.command.reset_cooldown(ctx)
                    return await main_msg.edit(content=f"{EMOJIS['tick_no']}Command cancelled.", embed=None, view=None)
                if view.value == 'add':
                    await main_msg.edit(embed=success_embed(
                        f"{EMOJIS['loading']} Rolemenu edit...",
                        f"{EMOJIS['tick_yes']} Please send the roles separated with a comma `,`.\n\nExample: `@Artist, @Foodie, @Music Lover, @Cutie`\nPlease follow this format."
                    ), view=None)
                    m = await wait_for_msg(ctx, 60, main_msg)
                    if m == 'pain':
                        return
                    roles_text_list = m.content.replace(" ", "").split(",")
                    roles = []
                    for role_text in roles_text_list:
                        try:
                            role = await commands.RoleConverter().convert(ctx, role_text)
                            if role.position < ctx.guild.me.top_role.position and (role.position < ctx.author.top_role.position or ctx.author == ctx.guild.owner) and role not in roles:
                                roles.append(role)
                        except Exception:
                            pass
                    if len(roles) == 0:
                        ctx.command.reset_cooldown(ctx)
                        return await main_msg.edit(embed=error_embed(
                            f"{EMOJIS['tick_no']} Error!",
                            f"Looks like no roles were found in your message.\nOr all the roles were above my top role.\nYou can join our **[Support Server]({SUPPORT_SERVER_LINK})** for help."
                        ))
                    await main_msg.edit(content="", embed=success_embed(
                        f"{len(roles)} Roles found!",
                        f"I have found **{len(roles)}** in your message.\n\n{' '.join(role.mention for role in roles)}\n\nNow you need to react to this message with the corresponding emojis for the rolemenu to be complete!"
                    ), view=None)
                    final_output = await prepare_emojis_and_roles(ctx, roles, main_msg)
                    if final_output is None:
                        return
                    current_role_menu = role_menus[str(message_id)]
                    stuff = current_role_menu['stuff']
                    for role_id, emoji in final_output.items():
                        stuff.update({role_id: emoji})
                    current_role_menu.update({"stuff": stuff})
                    role_menus.update({str(message_id): current_role_menu})
                    await self.client.self_roles.update_one(
                        filter={"_id": ctx.guild.id},
                        update={"$set": {"role_menus": role_menus}}
                    )
                    await prepare_rolemenu(ctx, stuff, self.client.get_channel(current_role_menu['channel']), current_role_menu['type'], message_id, edit=True)
                    return await main_msg.edit(content=f"{EMOJIS['tick_yes']}The rolemenu has been updated!", embed=None, view=None)
                if view.value == 'remove':
                    current_role_menu = role_menus[str(message_id)]
                    if len(current_role_menu['stuff']) == 1:
                        ctx.command.reset_cooldown(ctx)
                        return await main_msg.edit(embed=error_embed(
                            f"{EMOJIS['tick_no']} Error!",
                            "There's only one role in the rolemenu! You cannot remove that!"
                        ), view=None)
                    await main_msg.edit(embed=success_embed(
                        f"{EMOJIS['loading']} Rolemenu edit...",
                        f"{EMOJIS['tick_yes']} Please send the roles separated with a comma `,`.\n\nExample: `@Artist, @Foodie, @Music Lover, @Cutie`\nPlease follow this format."
                    ), view=None)
                    m = await wait_for_msg(ctx, 60, main_msg)
                    if m == 'pain':
                        return
                    roles_text_list = m.content.replace(" ", "").split(",")
                    roles = []
                    for role_text in roles_text_list:
                        try:
                            role = await commands.RoleConverter().convert(ctx, role_text)
                            if str(role.id) in role_menus[str(message_id)]['stuff']:
                                roles.append(role)
                        except Exception:
                            pass
                    if len(roles) == 0:
                        ctx.command.reset_cooldown(ctx)
                        return await main_msg.edit(embed=error_embed(
                            f"{EMOJIS['tick_no']} Error!",
                            f"Looks like no roles were found in your message.\nOr all the roles were above my top role.\nYou can join our **[Support Server]({SUPPORT_SERVER_LINK})** for help."
                        ))
                    stuff = current_role_menu['stuff']
                    for role in roles:
                        if str(role.id) in stuff:
                            stuff.pop(str(role.id))
                    current_role_menu.update({"stuff": stuff})
                    role_menus.update({str(message_id): current_role_menu})
                    await self.client.self_roles.update_one(
                        filter={"_id": ctx.guild.id},
                        update={"$set": {"role_menus": role_menus}}
                    )
                    await prepare_rolemenu(ctx, stuff, self.client.get_channel(current_role_menu['channel']), current_role_menu['type'], message_id, edit=True)
                    return await main_msg.edit(content=f"{EMOJIS['tick_yes']}The rolemenu has been updated!", embed=None, view=None)

            await ctx.reply(embed=info_embed)

    # @commands.command(help="Setup everything you'll ever need.")
    # @commands.has_permissions(administrator=True)
    # @commands.bot_has_permissions(administrator=True)
    # @commands.cooldown(3, 30, commands.BucketType.user)
    # @commands.max_concurrency(1, commands.BucketType.guild)
    # async def setup(self, ctx: commands.Context):
    #     return await ctx.reply("work in progress")

    @commands.cooldown(3, 60, commands.BucketType.user)
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(embed_links=True)
    @commands.command(aliases=['ap'], help="Configure autoposting for your server.")
    async def autopost(self, ctx: commands.Context, module=None, choice=None):
        msg = await ctx.reply(embed=discord.Embed(title=f"Working on it... {EMOJIS['loading']}"))
        prefix = ctx.clean_prefix
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        pain = guild_config['autoposting']
        autopost_module_limit = 5

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        if module is None or module.lower() in ['show']:
            embed = discord.Embed(
                title="🛠️  Your autoposting configuration",
                description=f"""
You have **{len(pain)}** autoposting modules enabled.
You can use `{prefix}autopost <module> enable/disable` to configure autoposting.
Please use `{prefix}autopost list` to view the autoposting modules list.
                """,
                color=MAIN_COLOR
            )
            uwu = ""  # sfw autoposting config
            owo = ""  # nsfw autoposting config haha horni hours
            for e in pain:
                thing = f"**{e['name'].title()}** - <#{e['channel_id']}>\n"
                if not e['nsfw']:
                    uwu += thing
                else:
                    owo += thing
            embed.add_field(name="SFW Posting Config:", value="None" if len(uwu) == 0 else uwu, inline=False)
            embed.add_field(name="NSFW Posting Config:", value="None" if len(owo) == 0 else owo, inline=False)
            return await msg.edit(embed=embed)
        elif module.lower() in ['list', 'l']:
            embed = success_embed(
                "🛠️  Available autoposting modules",
                f"""
You can use `{prefix}autopost <module> enable/disable` to configure autoposting.
Example: `{prefix}autopost meme enable`
                """
            )
            uwu = ""
            owo = ""
            for e in self.sfw_posting_modules:
                uwu += f"`{e}`, "
            for ee in self.nsfw_posting_modules:
                owo += f"`{ee}`, "
            so_much_pain = "Will only be shown in a **NSFW** channel."
            embed.add_field(name="SFW Modules:", value=uwu[:-2], inline=False)
            embed.add_field(name="NSFW Modules:", value=owo[:-2] if ctx.channel.is_nsfw() else so_much_pain, inline=False)
            return await msg.edit(embed=embed)
        elif module.lower() in self.sfw_posting_modules:
            hmm = await self.check_if_autopost_module_is_enabled_or_not(pain, module.lower())
            if hmm:
                if choice is not None and choice.lower() not in DISABLE:
                    ctx.command.reset_cooldown(ctx)
                    return await msg.edit(embed=error_embed(
                        f"{EMOJIS['tick_no']} Already enabled!",
                        f"""
The module `{module.lower()}` is already enabled.
Posting channel: <#{hmm['channel_id']}>

You can use `{prefix}autopost {module.lower()} disable` to disable it.
You can use `{prefix}autopost {module.lower()}` to edit the channel.
                        """
                    ))
                if choice is not None and choice.lower() in DISABLE:
                    pain.remove(hmm)
                    return await msg.edit(embed=success_embed(
                        f"{EMOJIS['tick_yes']} Disabled!",
                        f"The autoposting module `{module}` has now been disabled."
                    ))
            if choice is not None and choice.lower() in DISABLE:
                return await msg.edit(embed=success_embed(
                    f"{EMOJIS['tick_no']} Bruh!",
                    f"The autoposting for `{module.lower()}` is already disabled."
                ))
            if len(pain) >= autopost_module_limit and not hmm and ctx.guild.id not in PREMIUM_GUILDS:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Limit reached!",
                    f"You already have **{autopost_module_limit}** autoposting modules enabled!\nTo enable more you can ask for the owner's permissions by joining the **[Support Server]({SUPPORT_SERVER_LINK})**"
                ))
            await msg.edit(embed=success_embed(
                f"{EMOJIS['loading']} Enter a text channel for the `{module}` autoposting:",
                f"Make sure to mention the channel like this: {ctx.channel.mention}\nYou can also type `cancel` to cancel this."
            ))
            try:
                i_ran_out_ideas_for_variable_names = await self.client.wait_for("message", timeout=30, check=check)
            except asyncio.TimeoutError:
                ctx.command.reset_cooldown(ctx)
                return await msg.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Too slow!",
                    "You didn't answer in time. Please run the command again."
                ))
            if i_ran_out_ideas_for_variable_names.content.lower() == "cancel":
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=discord.Embed(title=f"{EMOJIS['tick_no']} Setup Cancelled!", color=RED_COLOR))
            try:
                # channel = await commands.TextChannelConverter.convert(ctx, i_ran_out_ideas_for_variable_names.content)
                c_id = int(i_ran_out_ideas_for_variable_names.content[2:-1])
            except Exception:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Channel!",
                    f"Please mention a channel properly, like this: {ctx.channel.mention}.\nPlease run the command again."
                ))
            channel = discord.utils.get(ctx.guild.channels, id=c_id)
            if channel is None:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=error_embed(
                    f"{EMOJIS['tick_no']} Channel Not Found!",
                    f"I wasn't able to find this channel: {i_ran_out_ideas_for_variable_names} please try again."
                ))
            if hmm:
                pain.remove(hmm)
            pain.append({
                "name": module.lower(),
                "channel_id": c_id,
                "nsfw": False
            })
            return await ctx.send(embed=success_embed(
                f"{EMOJIS['tick_yes']} Autoposting Set!",
                f"The autoposting channel for `{module.lower()}` is now set to <#{c_id}>."
            ))

        elif module.lower() in self.nsfw_posting_modules:
            if not ctx.channel.is_nsfw():
                ctx.command.reset_cooldown(ctx)
                return await msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} NSFW Only!",
                    "Please go to a **NSFW** channel to enable this module."
                ))
            hmm = await self.check_if_autopost_module_is_enabled_or_not(pain, module.lower())
            if hmm:
                if choice is not None and choice.lower() not in DISABLE:
                    ctx.command.reset_cooldown(ctx)
                    return await msg.edit(embed=error_embed(
                        f"{EMOJIS['tick_no']} Already enabled!",
                        f"""
The module `{module.lower()}` is already enabled.
Posting channel: <#{hmm['channel_id']}>

You can use `{prefix}autopost {module.lower()} disable` to disable it.
You can use `{prefix}autopost {module.lower()}` to edit the channel.
                        """
                    ))
                if choice is not None and choice.lower() in DISABLE:
                    pain.remove(hmm)
                    return await msg.edit(embed=success_embed(
                        f"{EMOJIS['tick_yes']} Disabled!",
                        f"The autoposting module `{module}` has now been disabled."
                    ))
            if choice is not None and choice.lower() in DISABLE:
                return await msg.edit(embed=success_embed(
                    f"{EMOJIS['tick_no']} Bruh!",
                    f"The autoposting for `{module.lower()}` is already disabled."
                ))
            if len(pain) >= autopost_module_limit and not hmm and ctx.guild.id not in PREMIUM_GUILDS:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Limit reached!",
                    f"You already have **{autopost_module_limit}** autoposting modules enabled!\nTo enable more you can ask for the owner's permissions by joining the **[Support Server]({SUPPORT_SERVER_LINK})**"
                ))
            await msg.edit(embed=success_embed(
                f"{EMOJIS['loading']} Enter a text channel for the `{module}` autoposting:",
                f"Make sure to mention the channel like this: {ctx.channel.mention}\nYou can also type `cancel` to cancel this."
            ))
            try:
                i_ran_out_ideas_for_variable_names = await self.client.wait_for("message", timeout=30, check=check)
            except asyncio.TimeoutError:
                ctx.command.reset_cooldown(ctx)
                return await msg.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Too slow!",
                    "You didn't answer in time. Please run the command again."
                ))
            if i_ran_out_ideas_for_variable_names.content.lower() == "cancel":
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=discord.Embed(title=f"{EMOJIS['tick_no']} Setup Cancelled!", color=RED_COLOR))
            try:
                # channel = await commands.TextChannelConverter.convert(ctx, i_ran_out_ideas_for_variable_names.content)
                c_id = int(i_ran_out_ideas_for_variable_names.content[2:-1])
            except Exception:
                return await ctx.send(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Channel!",
                    f"Please mention a channel properly, like this: {ctx.channel.mention}.\nPlease run the command again."
                ))
            channel = self.client.get_channel(c_id)
            if channel is None:
                return await ctx.send(embed=error_embed(
                    f"{EMOJIS['tick_no']} Channel Not Found!",
                    f"I wasn't able to find this channel: {i_ran_out_ideas_for_variable_names} please try again."
                ))
            if not channel.is_nsfw():
                return await ctx.send(embed=error_embed(
                    f"{EMOJIS['tick_no']} Channel not NSFW!",
                    f"The channel {channel.mention} needs to **NSFW** first!"
                ))
            if hmm:
                pain.remove(hmm)
            pain.append({
                "name": module.lower(),
                "channel_id": c_id,
                "nsfw": True
            })
            return await ctx.send(embed=success_embed(
                f"{EMOJIS['tick_yes']} Autoposting Set!",
                f"The autoposting channel for `{module.lower()}` is now set to <#{c_id}>."
            ))
        else:
            ctx.command.reset_cooldown(ctx)
            return await msg.edit(embed=error_embed(
                f"{EMOJIS['tick_no']} Not found!",
                f"The autoposting module `{module}` doesn't exist."
            ))

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_webhooks=True, manage_messages=True)
    @commands.command(help="Enable or Disable the NQN module.")
    async def nqn(self, ctx, *, choice=None):
        msg = await ctx.reply(embed=discord.Embed(title=f"Working on it... {EMOJIS['loading']}"))
        prefix = ctx.clean_prefix
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        pain = guild_config['nqn']
        yes_emoji = EMOJIS['tick_yes']
        no_emoji = EMOJIS['tick_no']
        if choice is None:
            return await msg.edit(embed=success_embed(
                f"{EMOJIS['cool']} NQN Mode is currently **{f'{yes_emoji}Enabled' if pain else f'{no_emoji}Disabled'}**",
                f"""
You can use `{prefix}nqn enable/disable` to enable or disable it.
                """
            ))
        if choice.lower() in ENABLE:
            if pain:
                return await msg.edit(embed=discord.Embed(
                    title=f"{EMOJIS['cool']} NQN Mode is already **{yes_emoji}Enabled**",
                    color=MAIN_COLOR
                ))
            guild_config['nqn'] = True
            return await msg.edit(embed=discord.Embed(
                title=f"{EMOJIS['cool']} NQN Mode is now **{yes_emoji}Enabled**",
                color=MAIN_COLOR
            ))
        elif choice.lower() in DISABLE:
            if not pain:
                return await msg.edit(embed=discord.Embed(
                    title=f"{EMOJIS['cool']} NQN Mode is already **{no_emoji}Disabled**",
                    color=MAIN_COLOR
                ))
            guild_config['nqn'] = False
            return await msg.edit(embed=discord.Embed(
                title=f"{EMOJIS['cool']} NQN Mode is now **{no_emoji}Disabled**",
                color=MAIN_COLOR
            ))
        else:
            return await msg.edit(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"`{choice}` is not a valid choice.\nCorrect Usage: `{prefix}nqn enable/disable`"
            ))

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.has_guild_permissions(manage_guild=True)
    @commands.command(aliases=['setprefix'], help="Change your server's prefix.")
    async def prefix(self, ctx: commands.Context, option: t.Optional[AddRemoveConverter] = None, *, prefix: t.Optional[Lower] = None):
        current_prefixes = await self.client.fetch_prefix(ctx.message)
        prefix_text = ""
        for prefix_ in current_prefixes:
            prefix_text += f"`{prefix_}`, "
        prefix_text = prefix_text[:-2]

        if option is None or not prefix:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['settings_color']} Custom prefixes",
                f"""
Your current prefixes are: {prefix_text}
You can also use `@{self.client.user.name}`

**Please use the following commands to add/remove prefixes:**

- `{ctx.clean_prefix}prefix add <prefix>` - Adds a new prefix.
- `{ctx.clean_prefix}prefix remove <prefix>` - Removes a prefix.
                """))

        if not option:
            if prefix not in current_prefixes:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(f"{EMOJIS['tick_no']}I wasn't able to find this prefix. Please try again.")
            if len(current_prefixes) == 1:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(f"{EMOJIS['tick_no']}You only have 1 prefix. You cannot remove this prefix until you add another one first.")
            for e in self.client.prefixes_cache:
                if e['_id'] == ctx.guild.id:
                    e['prefix'].remove(prefix)
                    return await ctx.reply(f"{EMOJIS['tick_yes']}The prefix `{prefix}` was removed.")

        if len(current_prefixes) >= 10:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(f"{EMOJIS['tick_no']}You can only have upto `10` prefixes.")

        if prefix in current_prefixes:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(f"{EMOJIS['tick_no']}This prefix is already added.")

        if len(prefix) > 20:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Too long!",
                "The maximum length of the prefix is **20**"
            ))

        prefix_cache = self.client.prefixes_cache

        for ee in prefix_cache:
            if ee['_id'] == ctx.guild.id:
                ee['prefix'].append(prefix)
                return await ctx.reply(f"{EMOJIS['tick_yes']}The prefix `{prefix}` has been added.")

    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(help="Disable a command category in your server!", aliases=['disable_category'])
    async def disablecategory(self, ctx: commands.Context, category: Category = None):
        if category is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                "Please specify a category to disable."
            ))
        category: commands.Cog = category  # dont mind me type hinting :scared:
        prefix = ctx.clean_prefix
        g = await self.client.get_guild_config(ctx.guild.id)
        disabled_categories: list = g.get('disabled_categories', [])
        if category.qualified_name in disabled_categories:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Already disabled!",
                f"The category `{category.qualified_name}` is already disabled."
            ).set_footer(text=f"You can use \"{prefix}disabled\" to get a list of all disabled commands/categories."))
        disabled_categories.append(category.qualified_name)
        g.update({'disabled_categories': disabled_categories})
        return await ctx.reply(embed=success_embed(
            f"{EMOJIS['tick_yes']} Category disabled!",
            f"The category `{category.qualified_name}` has been disabled."
        ).set_footer(text=f"You can use \"{prefix}disabled\" to get a list of all disabled commands/categories."))

    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(help="Enable a command category in your server!", aliases=['enable_category'])
    async def enablecategory(self, ctx: commands.Context, category: Category = None):
        if category is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                "Please specify a category to enable."
            ))
        category: commands.Cog = category
        prefix = ctx.clean_prefix
        g = await self.client.get_guild_config(ctx.guild.id)
        disabled_categories: list = g.get('disabled_categories', [])
        if category.qualified_name not in disabled_categories:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Already enabled!",
                f"The category `{category.qualified_name}` is already enabled."
            ).set_footer(text=f"You can use \"{prefix}disabled\" to get a list of all disabled commands/categories."))
        disabled_categories.remove(category.qualified_name)
        g.update({'disabled_categories': disabled_categories})
        return await ctx.reply(embed=success_embed(
            f"{EMOJIS['tick_yes']} Category enabled!",
            f"The category `{category.qualified_name}` has been enabled."
        ).set_footer(text=f"You can use \"{prefix}disabled\" to get a list of all disabled commands/categories."))

    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(3, 20, commands.BucketType.user)
    @commands.command(help="Disable a command in your server!")
    async def disable(self, ctx: commands.Context, setting: t.Union[discord.TextChannel, str] = None):
        prefix = ctx.clean_prefix
        if setting is None:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please mention a command/channel to disable it.\nCorrect Usage: `{prefix}disable command/#channel`"
            ))
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        if isinstance(setting, discord.TextChannel):
            if setting.id in guild_config['disabled_channels']:
                return await ctx.reply(f"{EMOJIS['tick_no']}This channel is already disabled.")
            amogus = guild_config['disabled_channels']
            amogus.append(setting.id)
            guild_config.update({"disabled_channels": amogus})
            return await ctx.reply(f"{EMOJIS['tick_yes']}Commands will no longer work in {setting.mention}.")
        if isinstance(setting, str):
            command = setting
            pain = self.client.get_command(command)
            if pain is None:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Command not found!",
                    f"I wasn't able to find any command named `{command}`"
                ))
            if pain.name in self.good_commands:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} No!",
                    f"`{command}` is one the core commands of EpicBot.\nYou cannot disable the command `{command}`"
                ))
            if pain.name in guild_config['disabled_cmds']:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already disabled!",
                    f"The command `{command}` is already disabled!"
                ))
            disabled_list = guild_config['disabled_cmds']
            disabled_list.append(pain.name)
            guild_config.update({"disabled_cmds": disabled_list})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Command Disabled!",
                f"The command `{command}` has now been disabled!"
            ))

    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(3, 20, commands.BucketType.user)
    @commands.command(help="Enable a command in your server!")
    async def enable(self, ctx: commands.Context, setting: t.Union[discord.TextChannel, str] = None):
        prefix = ctx.clean_prefix
        if setting is None:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please mention a command/channel to enable it.\nCorrect Usage: `{prefix}enable command/#channel`"
            ))
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        if isinstance(setting, discord.TextChannel):
            if setting.id not in guild_config['disabled_channels']:
                return await ctx.reply(f"{EMOJIS['tick_no']}This channel is already enabled.")
            amogus = guild_config['disabled_channels']
            amogus.remove(setting.id)
            guild_config.update({"disabled_channels": amogus})
            return await ctx.reply(f"{EMOJIS['tick_yes']}Commands will now function in {setting.mention}.")
        if isinstance(setting, str):
            command = setting
            pain = self.client.get_command(command)
            if pain is None:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Command not found!",
                    f"I wasn't able to find any command named `{command}`"
                ))
            if pain.name not in guild_config['disabled_cmds']:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already enabled!",
                    f"The command `{command}` is already enabled!"
                ))
            disabled_list = guild_config['disabled_cmds']
            disabled_list.remove(pain.name)
            guild_config.update({"disabled_cmds": disabled_list})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Command Enabled!",
                f"The command `{command}` has now been enabled!"
            ))

    @commands.command(
        aliases=['disabled', 'disablelist', 'dislist', 'disabledlist', 'disabled_cmds', 'disabledcmds', 'disabled_commands', 'disabledcommands'],
        help="Get a list of all the disabled commands."
    )
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def disabled_list(self, ctx: commands.Context):
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        cmds = guild_config['disabled_cmds']
        channels = guild_config['disabled_channels']
        categories = guild_config['disabled_categories']
        embed = success_embed(
            "Disabled list!",
            "These are all the disabled commands/channels/categories for this server!"
        )
        embed.add_field(
            name=f"[ {len(cmds)}/{len(self.client.commands)} ] Commands",
            value=', '.join(f"`{cmd}`" for cmd in cmds) or "No disabled commands :)",
            inline=False
        )
        embed.add_field(
            name=f"[ {len(channels)}/{len(ctx.guild.text_channels)} ] Channels",
            value='\n'.join(f"<#{channel}>" for channel in channels) or "No disabled channels :)",
            inline=False
        )
        embed.add_field(
            name=f"[ {len(categories)}/{len([cog for cog in self.client.cogs if cog.lower() == cog and len(self.client.get_cog(cog).get_commands()) != 0])} ] Categories",
            value=', '.join(f"`{category}`" for category in categories) or "No disabled categories :)",
            inline=False
        )

        return await ctx.reply(embed=embed)

    async def wait_for_msg(self, ctx: commands.Context, timeout, msg_to_edit) -> discord.Message:
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            msg = await self.client.wait_for(
                "message",
                timeout=timeout,
                check=check
            )
            try:
                await msg.delete()
            except Exception:
                pass
            if msg.content.lower() == 'cancel':
                ctx.command.reset_cooldown(ctx)
                await msg_to_edit.edit(embed=discord.Embed(
                    title=f"{EMOJIS['tick_no']} Cancelled!",
                    color=RED_COLOR
                ))
                return 'pain'
        except asyncio.TimeoutError:
            ctx.command.reset_cooldown(ctx)
            await msg_to_edit.edit(embed=error_embed(
                f"{EMOJIS['tick_no']} Too late!",
                "You didn't answer in time! Please re-run the command."
            ))
            return 'pain'
        return msg

    async def check_if_embed_is_shit_or_not_lmfao(self, ctx: commands.Context, temp_msg_cont, main_msg):
        prefix = ctx.clean_prefix
        try:
            embed_json = json.loads(temp_msg_cont)  # i have to add a check here to check if the THINGS inside the json is proper or not!
            test = await process_embeds_from_json(self.client, [ctx.author, ctx.guild], embed_json)
            make_sure_ur_embed_is_not_a_piece_of_shit = f"""
Here are a few things you should make sure before entering the embed:

- Make sure all the URLs are valid URLs.
- Make sure all the fields contain values.
- Make sure the embed has atleast a title/description/field.
- If you have an author/footer value make sure it contains a name/text value inside it.

If you think this isn't your fault and you found a bug please report it using `{prefix}bug`
For further problems you can join our **[Support Server]({SUPPORT_SERVER_LINK})**
            """

            if test == 'pain author name':
                await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Incomplete Embed!",
                    f"""
**Your embed is missing a `name` value inside of the `author` value.**
{make_sure_ur_embed_is_not_a_piece_of_shit}
                    """
                ).set_footer(text="Please re-run the command."))
                return 'pain'
            if test == 'pain footer text':
                await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Incomplete Embed!",
                    f"""
**Your embed is missing a `text` value inside of the `footer` value.**
{make_sure_ur_embed_is_not_a_piece_of_shit}
                    """
                ).set_footer(text="Please re-run the command."))
                return 'pain'
            if test == 'pain empty fields':
                await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Incomplete Embed!",
                    f"""
**Your fields are incomplete one of them either has a value of `""` or is missing a value completely.**
{make_sure_ur_embed_is_not_a_piece_of_shit}
                    """
                ).set_footer(text="Please re-run the command."))
                return 'pain'
            if test == 'pain invalid urls':
                await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Incomplete Embed!",
                    f"""
**One of your URLs is invalid and isn't a proper URL.**
Please make you enter proper URLs using `http` or `https`.
{make_sure_ur_embed_is_not_a_piece_of_shit}
                    """
                ).set_footer(text="Please re-run the command."))
                return 'pain'
            if test == 'pain empty embed':
                await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Incomplete Embed!",
                    f"""
Your embed is empty!
Please enter a complete embed with a description or a title.
{make_sure_ur_embed_is_not_a_piece_of_shit}
                    """
                ).set_footer(text="Please re-run the command."))
                return 'pain'
            else:
                return 'pog'
        except Exception:
            await main_msg.edit(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Embed Response!",
                "Please go to https://embedbuilder.nadekobot.me/ and paste a valid embed code next time!\nPlease re-run the command."
            ).set_image(url="https://nirlep-is.a-simp.xyz/b4aee7.png"))
            return 'pain'

    @commands.command(aliases=['cc', 'customcmd'], help="Configure custom commands for your server!")
    @commands.cooldown(5, 100, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def customcommand(self, ctx: commands.Context, option=None):
        prefix = ctx.clean_prefix
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        if "custom_cmds" not in guild_config:
            guild_config.update({"custom_cmds": []})
        custom_cmds_list = guild_config["custom_cmds"]
        custom_cmds_list_names_only = []
        for e in custom_cmds_list:
            custom_cmds_list_names_only.append(e['name'])
        if option is None:
            embed = success_embed(
                f"{EMOJIS['settings_color']} Custom Commands!",
                f"""
This server has **{len(custom_cmds_list)}** custom commands!

**You can use the following to configure custom commands:**

- `{prefix}cc create` - To create a custom command.
- `{prefix}cc delete` - To delete a custom command.
- `{prefix}cc show` - To show the list of all the custom commands.
- `{prefix}cc tags` - To get a list of all the custom tags.
                """
            )
            return await ctx.reply(embed=embed)
        if option.lower() in ['show', 'list', 'l']:
            return await ctx.invoke(self.client.get_command('customlist'))
        if option.lower() in ['create', 'make']:

            cc_limit = 25

            if len(custom_cmds_list) >= cc_limit and ctx.guild.id not in PREMIUM_GUILDS:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Too many commands!",
                    f"The maximum limit for custom commands is **{cc_limit}**.\nPlease delete some commands to create more."
                ))

            cmd_name = ""
            cmd_desc = ""
            cmd_reply = ""
            main_msg = await ctx.reply(embed=success_embed(
                f"{EMOJIS['loading']} Custom command process",
                "Please enter a name for your command."
            ))
            temp_msg_name = await self.wait_for_msg(ctx, 60, main_msg)  # waiting for a name
            if temp_msg_name == 'pain':
                return
            temp_msg_cont_name = temp_msg_name.content
            cmd = self.client.get_command(temp_msg_cont_name.lower())
            if cmd is not None or temp_msg_cont_name.lower() in custom_cmds_list_names_only:
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already Exists!",
                    f"A command named `{temp_msg_cont_name}` already exists.\nPlease re-run the command."
                ))
            if len(temp_msg_cont_name) > 25:
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Too long!",
                    "The command name can't be longer than **25** characters."
                ))
            useless_variable_totally = '_'.join(temp_msg_cont_name.lower().split(" "))
            cmd_name += useless_variable_totally

            await main_msg.edit(embed=success_embed(
                f"{EMOJIS['loading']} Custom command process",
                "Please enter a description for your command."
            ))
            temp_msg_desc = await self.wait_for_msg(ctx, 60, main_msg)  # waiting for a desc
            if temp_msg_desc == 'pain':
                return
            temp_msg_cont_desc = temp_msg_desc.content
            if len(temp_msg_cont_desc) > 250:
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Too long!",
                    "The command description can't be longer than **250** characters."
                ))
            cmd_desc += temp_msg_cont_desc

            await main_msg.edit(embed=success_embed(
                f"{EMOJIS['loading']} Custom command process",
                "**Do you want the reply to be an embed?**\n\nReply with `Yes` or `No`."  # checking if embed or not
            ).set_footer(text="If you are confused then reply with \"No\""))
            temp_msg_embed = await self.wait_for_msg(ctx, 60, main_msg)  # waiting for yes or no for embed
            if temp_msg_embed == 'pain':
                return
            temp_msg_cont_embed = temp_msg_embed.content
            if temp_msg_cont_embed.lower() in ['yes', 'true', 'yeah', 'y']:
                cmd_embed = True
            elif temp_msg_cont_embed.lower() in ['no', 'false', 'nope', 'n']:
                cmd_embed = False
            else:
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Response!",
                    "You didn't provide a valid answer.\nPlease re-run the command."
                ))

            for_embed_users_nerds = "\nGo to https://embedbuilder.nadekobot.me/ and paste the generated embed code here!\n"
            reeee = success_embed(
                f"{EMOJIS['loading']} Custom command process",
                f"""
Please type the response for your command here!{ for_embed_users_nerds if cmd_embed  else "" }
Here are the tags that you can use in custom commands:
{custom_cmds_tags_lemao}
                """
            ).set_footer(text="Please reply within 10 mins.")
            if cmd_embed:
                reeee.set_image(url="https://nirlep-is.a-simp.xyz/b4aee7.png")
            await main_msg.edit(embed=reeee)
            temp_msg = await self.wait_for_msg(ctx, 600, main_msg)  # waiting for the content
            if temp_msg == 'pain':
                return
            temp_msg_cont = temp_msg.content
            if cmd_embed:
                interesting_variable_name = await self.check_if_embed_is_shit_or_not_lmfao(ctx, temp_msg_cont, main_msg)
                if interesting_variable_name == 'pain':
                    return
            cmd_reply += temp_msg_cont
            custom_cmds_list.append({
                "name": cmd_name,
                "desc": cmd_desc,
                "reply": cmd_reply,
                "embed": cmd_embed
            })
            return await main_msg.edit(embed=success_embed(
                f"{EMOJIS['settings_color']} Custom Command Added!",
                f"The custom command with the name `{cmd_name}` has been added.\nYou can use `{prefix}clist` to see the list of all custom commands"
            ))

        if option.lower() in ['delete']:
            main_msg = await ctx.reply(embed=success_embed(
                f"{EMOJIS['loading']} Custom command deletion process",
                "Please enter the name of the command you want to delete."
            ))
            temp_msg = await self.wait_for_msg(ctx, 60, main_msg)
            if temp_msg == 'pain':
                return
            temp_msg_cont = temp_msg.content
            if temp_msg_cont.lower() not in custom_cmds_list_names_only:
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Not found!",
                    f"The custom command named `{temp_msg_cont}` does not exist."
                ))
            await main_msg.delete()
            view = Confirm(context=ctx)
            confirmation_msg = await ctx.reply(f"Are you sure you want to delete `{temp_msg_cont}`?", view=view)

            await view.wait()

            if view.value is None:
                return await confirmation_msg.edit(content="You didn't respond in time.", view=None)
            if not view.value:
                return await confirmation_msg.edit(content="Cancelled.", view=None)
            for e in custom_cmds_list:
                if e['name'] == temp_msg_cont.lower():
                    custom_cmds_list.remove(e)
            return await confirmation_msg.edit(content=f"The custom command named `{temp_msg_cont}` has been deleted.", view=None)

        if option.lower() in ['tags']:
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['settings_color']} Tags for custom commands!",
                f"Here are the tags you can use for custom commands: \n{custom_cmds_tags_lemao}"
            ))
        return await ctx.reply(embed=error_embed(
            f"{EMOJIS['tick_no']} Invalid Option!",
            f"That was not a valid option!\nPlease use `{prefix}cc` to see the valid options."
        ))

    @commands.command(aliases=['clist', 'customcmdslist'], help="Get a list of all custom commands!")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def customlist(self, ctx):
        prefix = ctx.clean_prefix
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        if "custom_cmds" not in guild_config:
            guild_config.update({"custom_cmds": []})
        custom_cmds_list = guild_config["custom_cmds"]
        if len(custom_cmds_list) == 0:
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['settings_color']} Custom commands list",
                f"There are no custom commands for this server!\nPlease use `{prefix}cc create` to create a custom command!"
            ))
        else:
            paginator = commands.Paginator(prefix="", suffix="", max_size=500)
            i = 1
            for e in custom_cmds_list:
                paginator.add_line(f"{i} - `{e['name']}` - {e['desc']}")
                i += 1
        embeds = []
        for page in paginator.pages:
            embeds.append(success_embed(
                f"{EMOJIS['settings_color']} Custom commands list",
                page
            ))
        if len(embeds) == 1:
            return await ctx.reply(embed=embeds[0])
        view = Paginator(ctx, embeds)
        return await ctx.reply(embed=embeds[0], view=view)

    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    @commands.command(help="Configure welcome messages for your server!")
    @commands.cooldown(4, 60, commands.BucketType.user)
    async def welcome(self, ctx, *, configuration=None):
        prefix = ctx.clean_prefix
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        welcome_config = guild_config['welcome']

        tick_yes = EMOJIS['tick_yes']
        tick_no = EMOJIS['tick_no']

        enabled = True if welcome_config['channel_id'] is not None else False

        if configuration is None:
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['settings_color']} Welcome Message Configuration!",
                f"""
Welcome messages are currently **{ tick_yes + " Enabled" if enabled else tick_no + " Disabled" }**

**To configure them you can use the following commands:**

- `{prefix}welcome {'disable' if enabled else 'enable'}`
- `{prefix}welcome channel`
- `{prefix}welcome message`
                """
            ))

        if configuration.lower() in ['enable', 'enabled']:
            if enabled:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already enabled!",
                    f"Welcome messages are already enabled and set to <#{welcome_config['channel_id']}>"
                ))
            welcome_channel = 0
            welcome_msg = ""
            main_msg = await ctx.reply(embed=success_embed(
                f"{EMOJIS['loading']} Welcome message configuration!",
                "Please mention the channel for welcome messages."
            ))
            temp_msg = await self.wait_for_msg(ctx, 30, main_msg)
            if temp_msg == 'pain':
                return
            temp_msg_cont = temp_msg.content
            try:
                c_id = int(temp_msg_cont[2:-1])
            except Exception:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Channel!",
                    f"Please mention a channel properly, like this: {ctx.channel.mention}.\nPlease run the command again."
                ))
            channel = discord.utils.get(ctx.guild.channels, id=c_id)
            if channel is None:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=error_embed(
                    f"{EMOJIS['tick_no']} Channel Not Found!",
                    f"I wasn't able to find this channel: {temp_msg_cont} please try again."
                ))
            welcome_channel += channel.id

            await main_msg.edit(embed=success_embed(
                f"{EMOJIS['loading']} Welcome message configuration!",
                "**Do you want to customize the welcome message?**\n\nReply with `Yes` or `No`."
            ).set_footer(text="If you are confused then reply with \"No\""))
            temp_msg = await self.wait_for_msg(ctx, 30, main_msg)
            if temp_msg == 'pain':
                return
            temp_msg_cont = temp_msg.content
            if temp_msg_cont.lower() in ['no', 'false', 'nope', 'n']:
                welcome_msg += DEFAULT_WELCOME_MSG
                welcome_embed = True
            elif temp_msg_cont.lower() in ['yes', 'true', 'yeah', 'y']:
                await main_msg.edit(embed=success_embed(
                    f"{EMOJIS['loading']} Welcome message configuration!",
                    "**Do you want the message to be an embed?**\n\nReply with `Yes` or `No`."
                ).set_footer(text="If you are confused then reply with \"No\""))
                temp_msg_embed = await self.wait_for_msg(ctx, 30, main_msg)
                if temp_msg_embed == 'pain':
                    return
                temp_msg_cont_embed = temp_msg_embed.content
                if temp_msg_cont_embed.lower() in ['yes', 'true', 'yeah', 'y']:
                    welcome_embed = True
                elif temp_msg_cont_embed.lower() in ['no', 'false', 'nope', 'n']:
                    welcome_embed = False
                else:
                    return await main_msg.edit(embed=error_embed(
                        f"{EMOJIS['tick_no']} Invalid Response!",
                        "You didn't provide a valid answer.\nPlease re-run the command."
                    ))
                for_embed_users_nerds = "\nGo to https://embedbuilder.nadekobot.me/ and paste the generated embed code here!\n"
                reeee = success_embed(
                    f"{EMOJIS['loading']} Welcome message configuration!",
                    f"""
Please type the welcome message here!{ for_embed_users_nerds if welcome_embed  else "" }
Here are the tags that you can use in custom commands:
{custom_cmds_tags_lemao}
                    """
                ).set_footer(text="Please reply within 10 mins.")
                if welcome_embed:
                    reeee.set_image(url="https://nirlep-is.a-simp.xyz/b4aee7.png")
                await main_msg.edit(embed=reeee)

                temp_msg = await self.wait_for_msg(ctx, 600, main_msg)  # waiting for the content
                if temp_msg == 'pain':
                    return
                temp_msg_cont = temp_msg.content
                if welcome_embed:
                    interesting_variable_name = await self.check_if_embed_is_shit_or_not_lmfao(ctx, temp_msg_cont, main_msg)
                    if interesting_variable_name == 'pain':
                        return
                    welcome_msg += temp_msg_cont
            else:
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Response!",
                    "You didn't provide a valid answer.\nPlease re-run the command."
                ))
            welcome_config.update({
                "channel_id": welcome_channel,
                "message": welcome_msg,
                "embed": welcome_embed
            })
            return await main_msg.edit(embed=success_embed(
                f"{EMOJIS['tick_yes']} Welcome Messages Configured!",
                f"Welcome messages will now be sent in <#{welcome_channel}>"
            ))

        if configuration.lower() in ['disable']:
            if not enabled:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already disabled!",
                    "Welcome messages are already disabled!"
                ))
            welcome_config.update({"channel_id": None})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Disabled!",
                "Welcome messages are now disabled!"
            ))

        if configuration.lower() in ['channel']:
            if not enabled:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Currently disabled!",
                    "Welcome messages are current disabled.\nPlease enable them to configure them."
                ))
            main_msg = await ctx.reply(embed=success_embed(
                f"{EMOJIS['loading']} Welcome channel!",
                f"The current welcome channel is <#{welcome_config['channel_id']}>\n\nPlease mention a channel to change it."
            ))
            temp_msg = await self.wait_for_msg(ctx, 60, main_msg)
            if temp_msg == 'pain':
                return
            temp_msg_cont = temp_msg.content
            try:
                c_id = int(temp_msg_cont[2:-1])
            except Exception:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Channel!",
                    f"Please mention a channel properly, like this: {ctx.channel.mention}.\nPlease run the command again."
                ))
            channel = discord.utils.get(ctx.guild.channels, id=c_id)
            if channel is None:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=error_embed(
                    f"{EMOJIS['tick_no']} Channel Not Found!",
                    f"I wasn't able to find this channel: {temp_msg_cont} please try again."
                ))
            welcome_config.update({"channel_id": channel.id})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Welcome channel updated!",
                f"The welcome channel is now set to {channel.mention}"
            ))

        if configuration.lower() in ['message', 'msg']:
            if not enabled:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Currently disabled!",
                    "Welcome messages are current disabled.\nPlease enable them to configure them."
                ))
            current_msg = welcome_config['message']
            embed_question_mark = welcome_config['embed']

            main_msg = await ctx.reply(embed=success_embed(
                f"{EMOJIS['loading']} Welcome message!",
                f"""
**Embed:** {tick_yes + ' Enabled' if embed_question_mark else tick_no + ' Disabled'}
Your current welcome message is this:
```
{current_msg}
```
In order to change it, please type a message here within 1 minute.
                """
            ))
            temp_msg = await self.wait_for_msg(ctx, 60, main_msg)
            if temp_msg == 'pain':
                return
            temp_msg_cont = temp_msg.content
            if embed_question_mark:
                interesting_variable_name = await self.check_if_embed_is_shit_or_not_lmfao(ctx, temp_msg_cont, main_msg)
                if interesting_variable_name == 'pain':
                    return
            welcome_config.update({"message": temp_msg_cont})
            return await main_msg.edit(embed=success_embed(
                f"{EMOJIS['tick_yes']} Welcome Message Updated!",
                "The welcome message has been successfully updated!"
            ))
        else:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Unknown option!",
                f"Please use `{prefix}welcome` to see all the available options."
            ))

    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    @commands.command(help="Configure leave messages for your server!")
    @commands.cooldown(4, 60, commands.BucketType.user)
    async def goodbye(self, ctx, *, configuration=None):
        prefix = ctx.clean_prefix
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        leave_config = guild_config['leave']

        tick_yes = EMOJIS['tick_yes']
        tick_no = EMOJIS['tick_no']

        enabled = True if leave_config['channel_id'] is not None else False

        if configuration is None:
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['settings_color']} Goodbye Message Configuration!",
                f"""
Goodbye messages are currently **{ tick_yes + " Enabled" if enabled else tick_no + " Disabled" }**

**To configure them you can use the following commands:**

- `{prefix}goodbye {'disable' if enabled else 'enable'}`
- `{prefix}goodbye channel`
- `{prefix}goodbye message`
                """
            ))

        if configuration.lower() in ['enable', 'enabled']:
            if enabled:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already enabled!",
                    f"Goodbye messages are already enabled and set to <#{leave_config['channel_id']}>"
                ))
            leave_channel = 0
            leave_msg = ""
            main_msg = await ctx.reply(embed=success_embed(
                f"{EMOJIS['loading']} Goodbye message configuration!",
                "Please mention the channel for leave messages."
            ))
            temp_msg = await self.wait_for_msg(ctx, 30, main_msg)
            if temp_msg == 'pain':
                return
            temp_msg_cont = temp_msg.content
            try:
                c_id = int(temp_msg_cont[2:-1])
            except Exception:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Channel!",
                    f"Please mention a channel properly, like this: {ctx.channel.mention}.\nPlease run the command again."
                ))
            channel = discord.utils.get(ctx.guild.channels, id=c_id)
            if channel is None:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=error_embed(
                    f"{EMOJIS['tick_no']} Channel Not Found!",
                    f"I wasn't able to find this channel: {temp_msg_cont} please try again."
                ))
            leave_channel += channel.id

            await main_msg.edit(embed=success_embed(
                f"{EMOJIS['loading']} Goodbye message configuration!",
                "**Do you want to customize the leave message?**\n\nReply with `Yes` or `No`."
            ).set_footer(text="If you are confused then reply with \"No\""))
            temp_msg = await self.wait_for_msg(ctx, 30, main_msg)
            if temp_msg == 'pain':
                return
            temp_msg_cont = temp_msg.content
            if temp_msg_cont.lower() in ['no', 'false', 'nope', 'n']:
                leave_msg += DEFAULT_LEAVE_MSG
                leave_embed = True
            elif temp_msg_cont.lower() in ['yes', 'true', 'yeah', 'y']:
                await main_msg.edit(embed=success_embed(
                    f"{EMOJIS['loading']} Goodbye message configuration!",
                    "**Do you want the message to be an embed?**\n\nReply with `Yes` or `No`."
                ).set_footer(text="If you are confused then reply with \"No\""))
                temp_msg_embed = await self.wait_for_msg(ctx, 30, main_msg)
                if temp_msg_embed == 'pain':
                    return
                temp_msg_cont_embed = temp_msg_embed.content
                if temp_msg_cont_embed.lower() in ['yes', 'true', 'yeah', 'y']:
                    leave_embed = True
                elif temp_msg_cont_embed.lower() in ['no', 'false', 'nope', 'n']:
                    leave_embed = False
                else:
                    return await main_msg.edit(embed=error_embed(
                        f"{EMOJIS['tick_no']} Invalid Response!",
                        "You didn't provide a valid answer.\nPlease re-run the command."
                    ))
                for_embed_users_nerds = "\nGo to https://embedbuilder.nadekobot.me/ and paste the generated embed code here!\n"
                reeee = success_embed(
                    f"{EMOJIS['loading']} Goodbye message configuration!",
                    f"""
Please type the leave message here!{ for_embed_users_nerds if leave_embed else "" }
Here are the tags that you can use in custom commands:
{custom_cmds_tags_lemao}
                    """
                ).set_footer(text="Please reply within 10 mins.")
                if leave_embed:
                    reeee.set_image(url="https://nirlep-is.a-simp.xyz/b4aee7.png")
                await main_msg.edit(embed=reeee)

                temp_msg = await self.wait_for_msg(ctx, 600, main_msg)  # waiting for the content
                if temp_msg == 'pain':
                    return
                temp_msg_cont = temp_msg.content
                if leave_embed:
                    interesting_variable_name = await self.check_if_embed_is_shit_or_not_lmfao(ctx, temp_msg_cont, main_msg)
                    if interesting_variable_name == 'pain':
                        return
                    leave_msg += temp_msg_cont
            else:
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Response!",
                    "You didn't provide a valid answer.\nPlease re-run the command."
                ))
            leave_config.update({
                "channel_id": leave_channel,
                "message": leave_msg,
                "embed": leave_embed
            })
            return await main_msg.edit(embed=success_embed(
                f"{EMOJIS['tick_yes']} Goodbye Messages Configured!",
                f"Goodbye messages will now be sent in <#{leave_channel}>"
            ))

        if configuration.lower() in ['disable']:
            if not enabled:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already disabled!",
                    "Goodbye messages are already disabled!"
                ))
            leave_config.update({"channel_id": None})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Disabled!",
                "Goodbye messages are now disabled!"
            ))

        if configuration.lower() in ['channel']:
            if not enabled:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Currently disabled!",
                    "Goodbye messages are current disabled.\nPlease enable them to configure them."
                ))
            main_msg = await ctx.reply(embed=success_embed(
                f"{EMOJIS['loading']} Goodbye channel!",
                f"The current leave channel is <#{leave_config['channel_id']}>\n\nPlease mention a channel to change it."
            ))
            temp_msg = await self.wait_for_msg(ctx, 60, main_msg)
            if temp_msg == 'pain':
                return
            temp_msg_cont = temp_msg.content
            try:
                c_id = int(temp_msg_cont[2:-1])
            except Exception:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Channel!",
                    f"Please mention a channel properly, like this: {ctx.channel.mention}.\nPlease run the command again."
                ))
            channel = discord.utils.get(ctx.guild.channels, id=c_id)
            if channel is None:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=error_embed(
                    f"{EMOJIS['tick_no']} Channel Not Found!",
                    f"I wasn't able to find this channel: {temp_msg_cont} please try again."
                ))
            leave_config.update({"channel_id": channel.id})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Goodbye channel updated!",
                f"The leave channel is now set to {channel.mention}"
            ))

        if configuration.lower() in ['message', 'msg']:
            if not enabled:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Currently disabled!",
                    "Goodbye messages are current disabled.\nPlease enable them to configure them."
                ))
            current_msg = leave_config['message']
            embed_question_mark = leave_config['embed']

            main_msg = await ctx.reply(embed=success_embed(
                f"{EMOJIS['loading']} Goodbye message!",
                f"""
**Embed:** {tick_yes + ' Enabled' if embed_question_mark else tick_no + ' Disabled'}
Your current leave message is this:
```
{current_msg}
```
In order to change it, please type a message here within 1 minute.
                """
            ))
            temp_msg = await self.wait_for_msg(ctx, 60, main_msg)
            if temp_msg == 'pain':
                return
            temp_msg_cont = temp_msg.content
            if embed_question_mark:
                interesting_variable_name = await self.check_if_embed_is_shit_or_not_lmfao(ctx, temp_msg_cont, main_msg)
                if interesting_variable_name == 'pain':
                    return
            leave_config.update({"message": temp_msg_cont})
            return await main_msg.edit(embed=success_embed(
                f"{EMOJIS['tick_yes']} Goodbye Message Updated!",
                "The leave message has been successfully updated!"
            ))
        else:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Unknown option!",
                f"Please use `{prefix}goodbye` to see all the available options."
            ))

    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    @commands.cooldown(3, 30, commands.BucketType.user)
    @commands.command(help="Configure autorole for your server.")
    async def autorole(self, ctx: commands.Context, setting=None, configuration=None, role: discord.Role = None):

        guild_config = await self.client.get_guild_config(ctx.guild.id)
        autorole_config = guild_config['autorole']
        prefix = ctx.clean_prefix

        valid_settings = ['humans', 'bots', 'all']
        valid_configurations = ['add', 'remove']

        human_settings = ""
        bot_settings = ""
        all_settings = ""

        if not autorole_config:
            guild_config.update({
                "autorole": {
                    "humans": [],
                    "bots": [],
                    "all": []
                }
            })
        autorole_config = guild_config['autorole']
        for e in autorole_config['humans']:
            human_settings += f"<@&{e}>, "
        human_settings = human_settings[:-2]
        for e in autorole_config['bots']:
            bot_settings += f"<@&{e}>, "
        bot_settings = bot_settings[:-2]
        for e in autorole_config['all']:
            all_settings += f"<@&{e}>, "
        all_settings = all_settings[:-2]

        if setting is None:
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['settings_color']} Autorole settings!",
                f"""
Here are your current settings:

**{EMOJIS['members']} Humans:** {human_settings if len(human_settings) != 0 else "`None`"}
**🤖  Bots:** {bot_settings if len(bot_settings) != 0 else "`None`"}
**{EMOJIS['tick_yes']} All:** {all_settings if len(all_settings) != 0 else "`None`"}

In order to configure your autorole settings, you can use the following commands.

`{prefix}autorole humans add/remove @role` - To add roles to new humans who join.
`{prefix}autorole bots add/remove @role` - To add roles to new bots who join.
`{prefix}autorole all add/remove @role` - To all roles to everyone who join.
"""
            ))
        if setting.lower() not in valid_settings:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid setting",
                f"`{setting}` is not a valid setting, the valid settings are `{', '.join(valid_settings)}`"
            ))
        correct_usage = f"\nCorrect Usage: `{prefix}autorole {setting} add/remove <role>`\nExample: `{prefix}autorole {setting} add @members`"
        if configuration is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Please enter a configuration!",
                f"Please enter a configuration next time!{correct_usage}"
            ))
        if configuration.lower() not in valid_configurations:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid configuration",
                f"`{setting}` is not a valid configuration, the valid configurations are `{', '.join(valid_configurations)}`{correct_usage}"
            ))
        if role is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Please mention a role!",
                f"Please mention a role OR the role ID next time!{correct_usage}"
            ))
        current_role_array = autorole_config[setting]
        if role.id in current_role_array and configuration.lower() == 'add':
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Already there!",
                "This role has already been added!"
            ))
        if role.id not in current_role_array and configuration.lower() == 'remove':
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Not found!",
                "This role has already been removed!"
            ))
        if configuration.lower() == 'add':
            if role.position >= ctx.guild.get_member(self.client.user.id).top_role.position:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Not enough perms!",
                    f"The role {role.mention} is higher than my top role!\nPlease give me a higher role than that role, so that I can give that role to new members."
                ))
            current_role_array.append(role.id)
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Added!",
                "The role will now be given to new members!"
            ))
        else:
            current_role_array.remove(role.id)
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Removed!",
                "The role will no longer be given to new members!"
            ))

    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(3, 30, commands.BucketType.user)
    @commands.command(help="Configure leveling system for your server!")
    async def leveling(self, ctx: commands.Context, configuration=None, choice=None, level=None, role: discord.Role = None):
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        prefix = ctx.clean_prefix
        leveling_config = guild_config['leveling']
        tick_yes = EMOJIS['tick_yes']
        tick_no = EMOJIS['tick_no']
        if "roles" not in leveling_config:
            leveling_config.update({"roles": {}})
        if "message" not in leveling_config:
            leveling_config.update({"message": None})
        embed = success_embed(
            f"{EMOJIS['leveling']} Leveling configuration!",
            f"""
Leveling system is currently **{tick_yes+'  Enabled' if leveling_config['enabled'] else tick_no+'  Disabled'}**
Level up channel: **{'<#'+str(leveling_config['channel_id'])+'>' if leveling_config['channel_id'] is not None else tick_no+'  None'}**
Level up message: `{DEFAULT_LEVEL_UP_MSG if leveling_config['message'] is None else leveling_config['message']}`

**To configure it you can use the following:**

- `{prefix}leveling {'disable' if leveling_config['enabled'] else 'enable'}` - To enable/disable leveling for this guild.
- `{prefix}leveling channel` - To change the level up channel.
- `{prefix}leveling message` - To change the level up message.
- `{prefix}leveling roles` - To manage level role rewards!
            """
        )
        if configuration is None:
            await ctx.reply(embed=embed)
            return
        if configuration.lower() == 'enable':
            if leveling_config['enabled']:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already enabled!",
                    "Leveling system is already enabled for this server."
                ))
            leveling_config.update({"enabled": True})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Enabled!",
                f"""
{EMOJIS['leveling']} Leveling config has now been enabled for this server!
You can configure the level up channel by using `{prefix}leveling channel`
You can configure the level up message by using `{prefix}leveling message`

Users can check their rank using `{prefix}rank`
Users can check the leaderboard using `{prefix}leaderboard`
                """
            ))
        if configuration.lower() == 'disable':
            if not leveling_config['enabled']:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already disabled!",
                    "Leveling system is already disabled for this server."
                ))
            leveling_config.update({"enabled": False})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Disabled",
                "Leveling system has been disabled for this server!"
            ))
        if configuration.lower() == 'channel':
            if not leveling_config['enabled']:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Not enabled!",
                    "Please enable leveling first to configure the level up channel."
                ))
            main_msg = await ctx.reply(embed=success_embed(
                f"{EMOJIS['loading']} Please enter a text channel!",
                "Enter a channel within 60 seconds to configure it!\nReply with `None` to remove channel."
            ))
            msg = await self.wait_for_msg(ctx, 60, main_msg)
            if msg == 'pain':
                return
            if msg.content.lower() == 'none':
                leveling_config.update({"channel_id": None})
                return await main_msg.edit(embed=success_embed(
                    f"{EMOJIS['tick_yes']} Channel removed!",
                    "The levelup channel was removed!"
                ))
            try:
                c_id = int(msg.content[2:-1])
            except Exception:
                ctx.command.reset_cooldown(ctx)
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Channel!",
                    f"Please mention a channel properly, like this: {ctx.channel.mention}.\nPlease run the command again."
                ))
            channel = discord.utils.get(ctx.guild.channels, id=c_id)
            if channel is None:
                ctx.command.reset_cooldown(ctx)
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Channel Not Found!",
                    f"I wasn't able to find this channel: {msg.content} please try again."
                ))
            leveling_config.update({"channel_id": channel.id})
            return await main_msg.edit(embed=success_embed(
                f"{EMOJIS['tick_yes']} Channel changed!",
                f"The levelup channel was successfully changed to: <#{c_id}>"
            ))
        if configuration.lower() == 'message':
            if not leveling_config['enabled']:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Not enabled!",
                    "Please enable leveling first to configure the level up message."
                ))
            main_msg = await ctx.reply(embed=success_embed(
                f"{EMOJIS['loading']} Level up message!",
                """
Enter the new message for level up announcements.

You can use the following tags in your message:

- `{user_name}` - The name of the user who just leveled up.
- `{user_nickname}` - The nickname of the user who just leveled up.
- `{user_discrim}` - The discrim of the user who just leveled up.
- `{user_tag}` - The complete tag of the user.
- `{user_mention}` - The mention of the user.
- `{user_id}` - The ID of the user.

- `{level}` - The current level of the user.
- `{messages}` - The message count of the user.

Reply with `None` if you want the default level up message.
                """
            ))
            msg = await self.wait_for_msg(ctx, 60, main_msg)
            if msg == 'pain':
                return
            if msg.content.lower() == 'none':
                leveling_config.update({"message": None})
                return await ctx.reply(embed=success_embed(
                    f"{EMOJIS['tick_yes']} Level up message updated!",
                    "The levelup message has now been reset!"
                ))
            leveling_config.update({"message": msg.content})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Level up message updated!",
                "The levelup message has now been updated!"
            ))
        if configuration.lower() == 'roles':
            if not leveling_config['enabled']:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Not enabled!",
                    "Please enable leveling first to configure the level up roles."
                ))
            if choice is None:
                roles_text = ""
                roles_text += "Members will be rewarded roles on reaching certain level!\n"
                roles_text += "You can configure these roles using the following commands:\n\n"

                roles_text += f"- `{prefix}leveling roles add <level> @role` - To add a level role!\n"
                roles_text += f"- `{prefix}leveling roles remove <level> @role` - To remove a level role!\n"

                roles_text += "\n**Current leveling roles:**\n\n"

                if len(leveling_config['roles']) != 0:
                    for e in leveling_config['roles']:
                        roles_text += f"Level {e} • <@&{leveling_config['roles'][e]}>\n"
                else:
                    roles_text += "No leveling roles :("

                embed = success_embed(
                    f"{EMOJIS['leveling']} Level roles!",
                    roles_text
                )
                return await ctx.reply(embed=embed)
            if choice.lower() in ['add', 'remove']:
                if level is None:
                    ctx.command.reset_cooldown(ctx)
                    return await ctx.reply(embed=error_embed(
                        f"{EMOJIS['tick_no']} Incomplete command!",
                        f"Make sure to enter all the arguements!\n\nCorrent Usage: `{prefix}leveling roles {choice.lower()} <level> @role`\nExample: `{prefix}leveling roles {choice.lower()} 5 @role`"
                    ))
                try:
                    level = int(level)
                    if level <= 0:
                        ctx.command.reset_cooldown(ctx)
                        return await ctx.reply(embed=error_embed(
                            f"{EMOJIS['tick_no']} Bruh!",
                            f"Levels can't negative or zero. {EMOJIS['weirdchamp']}"
                        ))
                except Exception:
                    ctx.command.reset_cooldown(ctx)
                    return await ctx.reply(embed=error_embed(
                        f"{EMOJIS['tick_no']} Not an integer!",
                        f"The level must be an integer!\n\nCorrent Usage: `{prefix}leveling roles {choice.lower()} <level> @role`\nExample: `{prefix}leveling roles {choice.lower()} 5 @role`"
                    ))
                if choice.lower() == 'add':
                    if str(level) in leveling_config['roles']:
                        ctx.command.reset_cooldown(ctx)
                        return await ctx.reply(embed=error_embed(
                            f"{EMOJIS['tick_no']} Already there!",
                            f"The level **{level}** already has a role reward!\nThe role <@&{leveling_config['roles'][str(level)]}> is the current role reward."
                        ))
                if choice.lower() == 'remove':
                    if str(level) not in leveling_config['roles']:
                        ctx.command.reset_cooldown(ctx)
                        return await ctx.reply(embed=error_embed(
                            f"{EMOJIS['tick_no']} Not found!",
                            f"The level **{level}** is not a role reward!"
                        ))
                if role is None and choice.lower() != 'remove':
                    ctx.command.reset_cooldown(ctx)
                    return await ctx.reply(embed=error_embed(
                        f"{EMOJIS['tick_no']} Please enter a role!",
                        f"You need to mention a role.\n\nCorrent Usage: `{prefix}leveling roles {choice.lower()} <level> @role`\nExample: `{prefix}leveling roles {choice.lower()} 5 @role`"
                    ))
                if choice.lower() != 'remove' and role.position >= ctx.guild.me.top_role.position:
                    ctx.command.reset_cooldown(ctx)
                    return await ctx.reply(embed=error_embed(
                        f"{EMOJIS['tick_no']} Role higher than me!",
                        f"The role {role.mention} is higher than my top role!\nPlease give me a higher role!"
                    ))

                if choice.lower() == 'add':
                    if len(leveling_config['roles']) >= 15 and ctx.guild.id not in PREMIUM_GUILDS:
                        return await ctx.reply(embed=error_embed(
                            f"{EMOJIS['tick_no']} Limit reached!",
                            "You can only have upto **15** leveling roles per guild!"
                        ))
                    leveling_config['roles'].update({str(level): role.id})
                    return await ctx.reply(embed=success_embed(
                        f"{EMOJIS['tick_yes']} Level role added!",
                        f"{role.mention} will be awarded to users upon reaching level **{level}**!"
                    ))
                if choice.lower() == 'remove':
                    leveling_config['roles'].pop(str(level))
                    return await ctx.reply(embed=success_embed(
                        f"{EMOJIS['tick_yes']} Level role removed!",
                        f"The role for level **{level}** has been removed!"
                    ))

            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid option!",
                "You can only `add` or `remove` a level role!"
            ))
        else:
            return await ctx.reply(embed=embed)

    @commands.command(help="Configure starboard for your server!", aliases=['sb'])
    @commands.cooldown(3, 30, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def starboard(self, ctx: commands.Context, configuration=None):
        prefix = ctx.clean_prefix
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        sb_config = guild_config['starboard']
        enabled = sb_config['enabled']
        if configuration is None:
            return await ctx.reply(embed=success_embed(
                "🌟  Starboard configuration!",
                f"""
**Starboard:** {'<#'+str(sb_config['channel_id'])+'>' if enabled else EMOJIS['tick_no']+'  Disabled'}
**Required Stars:** {sb_config['star_count']}

**You can use the following commands to configure starboard:**

- `{prefix}starboard {'disable' if enabled else 'enable'}` - To enable/disable starboard.
- `{prefix}starboard channel` - To change the starboard channel.
- `{prefix}starboard stars` - To change the required stars for starboard.
                """
            ))
        elif configuration.lower() in ['enable']:
            if enabled:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already enabled!",
                    f"Starboard is already enabled in channel: <#{sb_config['channel_id']}>"
                ))
            main_msg = await ctx.reply(embed=success_embed(
                f"{EMOJIS['loading']} Enter a channel...",
                "Mention a channel in which you want the starred messages to go to."
            ))
            m = await self.wait_for_msg(ctx, 60, main_msg)
            if m == 'pain':
                return
            try:
                c_id = int(m.content[2:-1])
            except Exception:
                ctx.command.reset_cooldown(ctx)
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Channel!",
                    f"Please mention a channel properly, like this: {ctx.channel.mention}.\nPlease run the command again."
                ))
            channel = discord.utils.get(ctx.guild.channels, id=c_id)
            if channel is None:
                ctx.command.reset_cooldown(ctx)
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Channel Not Found!",
                    f"I wasn't able to find this channel: {m.content} please try again."
                ))
            sb_config.update({"channel_id": channel.id})
            await main_msg.edit(embed=success_embed(
                f"{EMOJIS['loading']} Stars required",
                "Enter the number of stars required for a message to reach the starboard."
            ))
            m = await self.wait_for_msg(ctx, 60, main_msg)
            if m == 'pain':
                return
            try:
                star_count = int(m.content)
                if star_count <= 0:
                    return await ctx.reply(embed=error_embed(
                        f"{EMOJIS['weirdchamp']} Bruh!",
                        "The star count has to be greated than 0."
                    ).set_footer(text="smh"))
            except Exception:
                ctx.command.reset_cooldown(ctx)
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Integers only!",
                    "The star count should be an integer!\nPlease re-run the command and try again!"
                ))
            sb_config.update({"star_count": int(m.content)})
            sb_config.update({"enabled": True})
            return await main_msg.edit(embed=success_embed(
                "🌟  Starboard enabled!",
                f"The starboard has been set to <#{channel.id}>.\nMinimun star requirement is **{int(m.content)}** stars."
            ))
        elif configuration.lower() in ['disable']:
            if not enabled:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already disabled!",
                    "Starboard is already disabled!"
                ))
            sb_config.update({"enabled": False})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Disabled!",
                "Starboard has now been disabled!"
            ))
        elif configuration.lower() in ['channel']:
            if not enabled:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Starboard is disabled!",
                    "Please enable starboard first!"
                ))
            main_msg = await ctx.reply(embed=success_embed(
                f"{EMOJIS['loading']} Enter new channel!",
                f"The current starboard is <#{sb_config['channel_id']}>.\nEnter a new channel to change it!"
            ))
            m = await self.wait_for_msg(ctx, 60, main_msg)
            if m == 'pain':
                return
            try:
                c_id = int(m.content[2:-1])
            except Exception:
                ctx.command.reset_cooldown(ctx)
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Channel!",
                    f"Please mention a channel properly, like this: {ctx.channel.mention}.\nPlease run the command again."
                ))
            channel = discord.utils.get(ctx.guild.channels, id=c_id)
            if channel is None:
                ctx.command.reset_cooldown(ctx)
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Channel Not Found!",
                    f"I wasn't able to find this channel: {m.content} please try again."
                ))
            sb_config.update({"channel_id": channel.id})
            return await main_msg.edit(embed=success_embed(
                f"{EMOJIS['tick_yes']} Starboard channel updated!",
                f"The starboard channel has been set to {channel.mention}!"
            ))
        elif configuration.lower() in ['stars', 'star']:
            if not enabled:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Starboard is disabled!",
                    "Please enable starboard first!"
                ))
            main_msg = await ctx.reply(embed=success_embed(
                f"{EMOJIS['loading']} Enter new star requirement!",
                f"The current star requirement is **{sb_config['star_count']}**.\nEnter new star count to change it!"
            ))
            m = await self.wait_for_msg(ctx, 60, main_msg)
            if m == 'pain':
                return
            try:
                star_count = int(m.content)
                if star_count <= 0:
                    return await ctx.reply(embed=error_embed(
                        f"{EMOJIS['weirdchamp']} Bruh!",
                        "The star count has to be greated than 0."
                    ).set_footer(text="smh"))
            except Exception:
                ctx.command.reset_cooldown(ctx)
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} Integers only!",
                    "The star count should be an integer!\nPlease re-run the command and try again!"
                ))
            sb_config.update({"star_count": int(m.content)})
            return await main_msg.edit(embed=success_embed(
                "🌟  Star count updated!",
                f"The star count has now been updated to **{sb_config['star_count']}** stars!"
            ))
        else:
            return await ctx.invoke(self.client.get_command('starboard'))

    @commands.command(
        help="Enable server logging so you know what exactly is going on in your server!",
        aliases=['mod-logs', 'logs', 'logging', 'modlog']
    )
    @commands.cooldown(3, 30, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(administrator=True)
    async def modlogs(self, ctx: commands.Context, channel: t.Union[discord.TextChannel, str] = None):
        prefix = ctx.clean_prefix
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        log_chan = guild_config['logging']

        embed = success_embed(
            "📝  Mod logs!",
            f"""
Logging is currently {'set in ' if log_chan is not None else ''}**{EMOJIS['tick_no']+'  Disabled' if log_chan is None else '<#'+str(log_chan)+'>'}**

**You can use the following commands to configure mod logs:**

- `{prefix}modlogs #channel` - To set/change the log channel.
- `{prefix}modlogs disable` - To disable mod logs.
            """
        )

        if channel is None:
            return await ctx.reply(embed=embed)
        if isinstance(channel, discord.TextChannel):
            guild_config.update({"logging": channel.id})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Log channel updated!",
                f"The log channel has been updated to {channel.mention}"
            ))
        if channel.lower() in ['disable']:
            guild_config.update({"logging": None})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Logs disabled!",
                "Mod logs have been disabled!"
            ))
        return await ctx.reply(embed=embed)

    @commands.command(help="Setup a ticket creation channel.")
    @commands.has_permissions(manage_guild=True, manage_channels=True, manage_threads=True)
    @commands.bot_has_permissions(administrator=True)
    @commands.cooldown(3, 120, commands.BucketType.guild)
    async def ticket(self, ctx: commands.Context, option: t.Union[discord.TextChannel, str] = None, *, setting: t.Union[discord.Role, str] = None):

        if 'PRIVATE_THREADS' not in ctx.guild.features:
            return await ctx.reply(f"{EMOJIS['tick_no']}Unfortunately, private threads are not enabled in your server...\nYou cannot use this command without `PRIVATE_THREADS`")

        async def please_enable():
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(f"{EMOJIS['tick_no']}You need to enable ticket system to use this command.\n{EMOJIS['arrow']}Please use `{ctx.clean_prefix}ticket enable` to enable it.")

        g = await self.client.get_guild_config(ctx.guild.id)
        if "roles" not in g['tickets']:
            g['tickets'].update({"roles": []})
        t_channel = self.client.get_channel(g['tickets']['channel'])
        if t_channel is not None:
            try:
                t_msg = await t_channel.fetch_message(g['tickets']['message_id'])
            except discord.NotFound:
                t_msg = None
        else:
            t_msg = None
        enabled = False if not t_msg else True
        t_roles = ""
        for role in g['tickets']['roles']:
            t_roles += f"<@&{role}> "
        info_embed = success_embed(
            "🎟️ Ticket System",
            f"""
**Ticket system is currently {'Disabled' if not enabled else '[Enabled]('+ str(t_msg.jump_url) +')'}**

Here are the commands that you can use to configure ticket system:

- `{ctx.clean_prefix}ticket enable/disable` - To enable/disable the ticket system.
- `{ctx.clean_prefix}ticket #channel` - To change the ticket panel channel.
- `{ctx.clean_prefix}ticket message <message>` - To change the default ticket panel message.
- `{ctx.clean_prefix}ticket add/remove @role` - To add/remove a ticket role.
- `{ctx.clean_prefix}ticket close` - To close a current ticket.

Ticket roles: {t_roles if len(t_roles) != 0 else 'No roles.'}
            """
        )
        if option is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=info_embed)
        if isinstance(option, discord.TextChannel):
            if not enabled:
                return await please_enable()
            if t_msg is not None:
                await t_msg.delete()
            msg = await option.send(embed=success_embed(
                "🎟️ Tickets",
                "Click the button to open a ticket."
            ), view=TicketView())
            g['tickets'].update({
                "channel": option.id,
                "message_id": msg.id
            })
            return await ctx.reply(f"{EMOJIS['tick_yes']}The ticket channel has been updated to {option.mention}")
        if option.lower() in ['enable', 'on', 'yes']:
            if enabled:
                return await ctx.reply(f"{EMOJIS['tick_no']}Ticket system is already enabled.")
            main_msg = await ctx.reply(embed=success_embed(
                f"{EMOJIS['loading']} Ticket System Process...",
                "Please enter a text channel for the ticket panel.\nReply with `create` if you want to create one."
            ))
            m = await self.wait_for_msg(ctx, 60, main_msg)
            if m == 'pain':
                return
            t_overwrites = {
                ctx.guild.me: discord.PermissionOverwrite(
                    send_messages=True,
                    create_public_threads=True,
                    create_private_threads=True
                ),
                ctx.guild.default_role: discord.PermissionOverwrite(
                    send_messages=False,
                    create_public_threads=False,
                    create_private_threads=True
                )
            }
            if m.content.lower() == 'create':
                channel = await ctx.guild.create_text_channel(
                    'tickets',
                    reason="Ticket system for EpicBot.",
                    topic="EpicBot Ticket System.\nClick the button to open a ticket.",
                    overwrites=t_overwrites
                )
            else:
                try:
                    channel = await commands.TextChannelConverter().convert(ctx, m.content)
                except Exception:
                    await main_msg.delete()
                    raise commands.ChannelNotFound(m.content)
                await channel.edit(overwrites=t_overwrites, reason="Ticket system for EpicBot.")
            await main_msg.edit(embed=success_embed(
                f"{EMOJIS['loading']} Ticket System Process...",
                "Please type a custom message for the ticket panel.\nReply with `None` if you don't want a custom message."
            ))
            m = await self.wait_for_msg(ctx, 60, main_msg)
            if m == 'pain':
                return
            custom_msg = m.content if m.content.lower() != 'none' else 'Click the button to open a ticket!'

            m_ = await channel.send(embed=success_embed("🎟️ Tickets", custom_msg), view=TicketView())
            g['tickets'].update({
                "channel": channel.id,
                "message_id": m_.id
            })
            return await main_msg.edit(embed=success_embed(
                f"{EMOJIS['tick_yes']} The ticket setup is complete!",
                f"Users will now be able to create tickets using **[this panel]({m_.jump_url})**\n\nIf you want to add roles that can always view all the tickets then please use `{ctx.clean_prefix}ticket add @role`"
            ))
        if option.lower() in ['disable', 'off', 'no']:
            if not enabled:
                return await please_enable()
            channel = self.client.get_channel(g['tickets']['channel'])
            if channel is not None:
                try:
                    msg = await channel.fetch_message(g['tickets']['message_id'])
                    await msg.delete()
                except Exception:
                    pass
            g['tickets'].update({
                "channel": None,
                "message_id": None,
                "roles": []
            })
            return await ctx.reply(f"{EMOJIS['tick_yes']}Ticket system has now been disabled.")
        if option.lower() in ['message', 'msg']:
            if not enabled:
                return await please_enable()
            if setting is None:
                return await ctx.reply(f"Correct Usage: `{ctx.clean_prefix}ticket message <message>`")
            channel = self.client.get_channel(g['tickets']['channel'])

            async def pain():
                g['tickets'].update({
                    "channel": None,
                    "message_id": None
                })
                return await ctx.reply(f"{EMOJIS['tick_no']}Looks like the preview panel has been deleted.\n{EMOJIS['arrow']}Please run the `{ctx.clean_prefix}ticket enable` command again to setup a new one.")
            if channel is None:
                await pain()
            try:
                msg_ = await channel.fetch_message(g['tickets']['message_id'])
                await msg_.edit(embed=success_embed("🎟️ Tickets", str(setting)), view=TicketView())
                return await ctx.reply(f"{EMOJIS['tick_yes']}The ticket panel has been updated.")
            except Exception:
                await pain()
        if option.lower() in ['addrole', 'add_role', 'add']:
            if not enabled:
                return await please_enable()
            if setting is None:
                return await ctx.reply(f"Correct Usage: `{ctx.clean_prefix}ticket {option.lower()} @role`")
            if not isinstance(setting, discord.Role):
                raise commands.RoleNotFound(setting)
            amogus = g['tickets']['roles']
            if setting.id in amogus:
                return await ctx.reply(f"Role {setting.mention} is already a ticket role.")
            amogus.append(setting.id)
            g['tickets'].update({"roles": amogus})
            return await ctx.reply(f"{EMOJIS['tick_yes']}Role added.")
        if option.lower() in ['removerole', 'remove_role', 'remove']:
            if not enabled:
                return await please_enable()
            if setting is None:
                return await ctx.reply(f"Correct Usage: `{ctx.clean_prefix}ticket {option.lower()} @role`")
            if not isinstance(setting, discord.Role):
                raise commands.RoleNotFound(setting)
            amogus = g['tickets']['roles']
            if setting.id not in amogus:
                return await ctx.reply(f"Role {setting.mention} isn't a ticket role.")
            amogus.remove(setting.id)
            g['tickets'].update({"roles": amogus})
            return await ctx.reply(f"{EMOJIS['tick_yes']}Role removed.")
        if option.lower() == 'close':
            async def not_ticket():
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(f"{EMOJIS['tick_no']}This is not a ticket.")
            if not isinstance(ctx.channel, discord.Thread):
                return await not_ticket()
            if not ctx.channel.name.startswith("ticket-"):
                return await not_ticket()
            await ctx.message.add_reaction(EMOJIS['tick_yes'][:-1])
            return await ctx.channel.edit(archived=True)
        return await ctx.reply(embed=info_embed)

    @commands.command(help="Set a chatbot channel for your server!")
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def chatbot(self, ctx, channel: t.Union[discord.TextChannel, str] = None):
        prefix = ctx.clean_prefix
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        chat_chan = guild_config['chatbot']

        embed = success_embed(
            f"{EMOJIS['chat']} Chatbot!",
            f"""
Chatbot is currently {'set in ' if chat_chan is not None else ''}**{EMOJIS['tick_no']+'  Disabled' if chat_chan is None else '<#'+str(chat_chan)+'>'}**

**You can use the following commands to configure chatbot:**

- `{prefix}chatbot #channel` - To set/change the chatbot channel.
- `{prefix}chatbot disable` - To disable chatbot.
            """
        )

        if channel is None:
            return await ctx.reply(embed=embed)
        if isinstance(channel, discord.TextChannel):
            guild_config.update({"chatbot": channel.id})
            await channel.edit(slowmode_delay=5)
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Chatbot channel updated!",
                f"The chatbot channel has been updated to {channel.mention}"
            ))
        if channel.lower() in ['disable']:
            guild_config.update({"chatbot": None})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Chatbot disabled!",
                "Chatbot has been disabled!"
            ))
        return await ctx.reply(embed=embed)

    @commands.command(help="Configure global chat for your server!")
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_channels=True, manage_webhooks=True)
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def globalchat(self, ctx, setting: t.Union[discord.TextChannel, str] = None):
        g = await self.client.get_guild_config(ctx.guild.id)
        prefix = ctx.clean_prefix
        gc = g['globalchat']
        enabled = False if not gc else True

        info_embed = success_embed(
            "🌍  Global Chat",
            f"""
Global chat is currently {'**Disabled**' if not enabled else 'set in <#'+str(gc)+'>'}

**Here are the commands related to global chat:**

- `{prefix}globalchat #channel` - To enable globalchat / update globalchat channel.
- `{prefix}globalchat disable` - To disable globalchat.
- `{prefix}globalchat rules` - Read the rules (please).

- `{prefix}report @user/<userid>/username` - To report a user.
            """
        )

        if setting is None:
            return await ctx.reply(embed=info_embed)
        if isinstance(setting, discord.TextChannel):
            view = Confirm(context=ctx)
            m = await ctx.reply(embed=success_embed(
                "🌍  Do you agree to the global chat rules?",
                GLOBAL_CHAT_RULES
            ), view=view)

            await view.wait()

            if view.value is None:
                return await m.edit(
                    embed=error_embed(f"{EMOJIS['tick_no']} Too late!", "You didn't respond in time"),
                    view=None
                )
            if not view.value:
                return await m.edit(
                    embed=error_embed(f"{EMOJIS['tick_no']} You didn't agree!", "You didn't agree to the global chat rules."),
                    view=None
                )
            await setting.edit(slowmode_delay=5)
            g.update({"globalchat": setting.id})
            return await m.edit(
                embed=success_embed(
                    f"{EMOJIS['tick_yes']} Global chat!",
                    f"The global chat has been set to {setting.mention}.\nHave fun chatting with people :D"
                ),
                view=None
            )

        if setting.lower() in ['disable', 'off']:
            if not enabled:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already disabled!",
                    "Global chat is already disabled."
                ))
            g.update({"globalchat": False})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Global chat disabled.",
                "Global chat has now been disabled."
            ))
        if setting.lower() in ['rules']:
            return await ctx.reply(GLOBAL_CHAT_RULES)
        return await ctx.reply(embed=info_embed)

    @commands.command(help="Enable counting in your server!")
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_channels=True, manage_messages=True)
    @commands.cooldown(3, 30, commands.BucketType.guild)
    async def counting(self, ctx: commands.Context, setting: t.Union[discord.TextChannel, str] = None):
        g = await self.client.get_guild_config(ctx.guild.id)
        enabled = False if not g['counting'] else True
        info_embed = success_embed(
            ":1234: Counting!",
            f"""
Counting is currently **{'Disabled' if not enabled else 'set in <#'+str(g['counting']['channel'])+'>'}**.

**Here are the commands you can use to configure counting:**

- `{ctx.clean_prefix}counting #channel` - To enable/change the counting channel.
- `{ctx.clean_prefix}counting disable` - To disable counting.
- `{ctx.clean_prefix}setcount <number>` - To set the count for the server.
            """
        )
        if setting is None:
            return await ctx.reply(embed=info_embed)
        if isinstance(setting, discord.TextChannel):
            g.update({"counting": {
                "channel": setting.id,
                "count": 0 if not enabled else g['counting']['count'],
                "last_user": None,
                "count_msg": None
            }})
            await setting.send(f"This channel is now set as the counting channel.\nThe current count is `{g['counting']['count']}`")
            await setting.edit(slowmode_delay=5)
            return await ctx.reply(f"{EMOJIS['tick_yes']} The counting channel has been updated to: {setting.mention}")
        if setting.lower() == 'disable':
            g.update({"counting": None})
            return await ctx.reply(f"{EMOJIS['tick_yes']} Counting has now been disabled.")
        return await ctx.reply(embed=info_embed)

    @commands.command(help="Set the count to any number.")
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def setcount(self, ctx, number=None):
        if number is None:
            return await ctx.reply(f"Correct Usage: `{ctx.clean_prefix}setcount <number>`\nExample: `{ctx.clean_prefix}setcount 69420`")
        try:
            number = int(number)
            if number <= 0:
                return await ctx.reply("Bruh, enter positive values ._.")
        except Exception:
            return await ctx.reply("Please enter numbers ._.")
        g = await self.client.get_guild_config(ctx.guild.id)
        if g['counting'] is None:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Counting not enabled!",
                f"You need to enable counting in order to use this command.\nPlease use `{ctx.clean_prefix}counting` for more info."
            ))
        before_count = g['counting']['count']
        g['counting'].update({"count": number})
        return await ctx.reply(f"The count has been updated: `{before_count}` ➜ `{number}`")

    # @commands.command(help="Setup server counters!")
    # @commands.has_permissions(manage_guild=True, manage_channels=True)
    # @commands.bot_has_permissions(manage_channels=True, manage_messages=True)
    # @commands.cooldown(3, 30, commands.BucketType.guild)
    # async def counters(self, ctx: commands.Context):
    #     pass

    @commands.command(help="Configure automod for your server!", aliases=['am'])
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(administrator=True)
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def automod(self, ctx, module=None, setting=None, other: t.Union[discord.Role, discord.TextChannel, str] = None):

        g = await self.client.get_guild_config(ctx.guild.id)
        prefix = ctx.clean_prefix
        am = g['automod']
        tick_yes = EMOJIS['tick_yes']
        tick_no = EMOJIS['tick_no']

        available_modules = []
        am_modules_text = ""
        cancer = ['ignored_channels', 'allowed_roles']

        for e in DEFAULT_AUTOMOD_CONFIG:
            if e not in cancer:
                available_modules.append(e)
        for e in available_modules:
            am_modules_text += f"{e}, "

        am_modules_text = am_modules_text[:-2]

        am_settings = ""

        for e in am:
            if e not in cancer:
                am_settings += f"**{e.replace('_', ' ').title()}:** {tick_yes+'  Enabled' if am[e]['enabled'] else tick_no+'  Disabled'}\n"

        good_roles = ""
        good_channels = ""

        for r in am['allowed_roles']:
            good_roles += f"<@&{r}> "
        for c in am['ignored_channels']:
            good_channels += f"<#{c}> "

        embed = success_embed(
            f"{BADGE_EMOJIS['bot_mod']}  Automod Configuration",
            f"""
**Here are you automod settings:**\n\n{am_settings}
**Here are the available modules:**```{am_modules_text}```
**Allowed Roles:** {good_roles if good_roles != "" else "None"}
**Ignored Channels:** {good_channels if good_channels != "" else "None"}

**In order to configure a module you can use:**

- `{prefix}automod <module> enable/disable` - Enable or disable a specific module.
- `{prefix}automod all enable/disable` - Enable or disable all modules.

- `{prefix}automod roles add/remove <role>` - To add/remove a role from whitelist.
- `{prefix}automod channel add/remove <channel>` - To add/remove a channel from whitelist.
- `{prefix}automod links add/remove <link>` - To add/remove links from whitelist.
- `{prefix}automod badwords add/remove <word>` - To add/remove bad words.
- `{prefix}automod badwords show` - To get a list of all badwords.
            """
        )

        reeeee = ["all", 'roles', 'channel', 'links', 'badwords']

        if module is None:
            return await ctx.reply(embed=embed)
        if module.lower() not in available_modules and module.lower() not in reeeee:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Unknown Module!",
                f"Here are the available modules:```{am_modules_text}```\nPlease enter a valid module."
            ))

        if module.lower() == 'roles':
            em = success_embed(
                f"{BADGE_EMOJIS['bot_mod']}  Automod allowed roles",
                f"The current allowed roles are:\n{good_roles if good_roles != '' else 'None'}\n\nUse `{prefix}automod roles add/remove <role>`"
            )
            if setting is None or setting.lower() not in ['add', 'remove'] or other is None:
                return await ctx.reply(embed=em)
            if not isinstance(other, discord.Role):
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Not found!",
                    "I wasn't able to find that role, please try again!"
                ))
            if other.id in am['allowed_roles'] and setting.lower() == 'add':
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already there!",
                    "This role is already a allowed role!"
                ))
            if other.id not in am['allowed_roles'] and setting.lower() == 'remove':
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Not there!",
                    "This role is not a allowed role!"
                ))
            if setting.lower() == 'add':
                old_roles_list = am['allowed_roles']
                old_roles_list.append(other.id)
                am.update({"allowed_roles": old_roles_list})
                return await ctx.reply(embed=success_embed(
                    f"{EMOJIS['tick_yes']} Role added!",
                    f"Users with role {other.mention} will no longer trigger automod."
                ))
            if setting.lower() == 'remove':
                old_roles_list = am['allowed_roles']
                old_roles_list.remove(other.id)
                am.update({"allowed_roles": old_roles_list})
                return await ctx.reply(embed=success_embed(
                    f"{EMOJIS['tick_yes']} Role removed!",
                    f"Users with role {other.mention} will now trigger automod."
                ))
        if module.lower() == 'channel':
            em = success_embed(
                f"{BADGE_EMOJIS['bot_mod']}  Automod ignored channels",
                f"The current ignored channels are:\n{good_channels if good_channels != '' else 'None'}\n\nUse `{prefix}automod channel add/remove <channel>`"
            )
            if setting is None or setting.lower() not in ['add', 'remove'] or other is None:
                return await ctx.reply(embed=em)
            if not isinstance(other, discord.TextChannel):
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Not found!",
                    "I wasn't able to find that channel, please try again!"
                ))
            if other.id in am['ignored_channels'] and setting.lower() == 'add':
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already there!",
                    "This channel is already a ignored channel!"
                ))
            if other.id not in am['ignored_channels'] and setting.lower() == 'remove':
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Not there!",
                    "This role is not a ignored channel!"
                ))
            if setting.lower() == 'add':
                old_roles_list = am['ignored_channels']
                old_roles_list.append(other.id)
                am.update({"ignored_channels": old_roles_list})
                return await ctx.reply(embed=success_embed(
                    f"{EMOJIS['tick_yes']} Channel added!",
                    f"Users in channel {other.mention} will no longer trigger automod."
                ))
            if setting.lower() == 'remove':
                old_roles_list = am['ignored_channels']
                old_roles_list.remove(other.id)
                am.update({"ignored_channels": old_roles_list})
                return await ctx.reply(embed=success_embed(
                    f"{EMOJIS['tick_yes']} Role removed!",
                    f"Users in channel {other.mention} will now trigger automod."
                ))
        if module.lower() == 'links':
            return await ctx.reply("This is work in progress!")
        if module.lower() == 'badwords':
            return await ctx.reply("This is work in progress!")
        if setting is None:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Incorrect Usage!",
                f"Correct Usage: `{prefix}automod {module.lower()} enable/disable`"
            ))
        if setting.lower() not in ['enable', 'disable']:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Incorrect Usage!",
                f"Correct Usage: `{prefix}automod {module.lower()} enable/disable`"
            ))
        if module.lower() != "all":
            module_dict = am[module.lower()]
            module_dict.update({"enabled": True if setting.lower() == 'enable' else False})
            am.update({module.lower(): module_dict})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Module {'Enabled' if setting.lower() == 'enable' else 'Disabled'}",
                f"The automod module `{module.lower()}` has been **{tick_yes+'  Enabled' if setting.lower() == 'enable' else tick_no+'  Disabled'}**"
            ))
        for module in available_modules:
            module_dict = am[module.lower()]
            module_dict.update({"enabled": True if setting.lower() == 'enable' else False})
            am.update({module.lower(): module_dict})
        return await ctx.reply(embed=success_embed(
            f"{EMOJIS['tick_yes']} All modules {'Enabled' if setting.lower() == 'enable' else 'Disabled'}",
            f"All automod modules have been **{tick_yes+'  Enabled' if setting.lower() == 'enable' else tick_no+'  Disabled'}**"
        ))

    @commands.command(aliases=['ghostpings', 'whoping', 'whopinged'], help="Configure ghost pings for your server!")
    @commands.cooldown(3, 15, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def ghostping(self, ctx):
        g = await self.client.get_guild_config(ctx.guild.id)
        g.update({"ghost_ping": False if g['ghost_ping'] else True})
        p = g['ghost_ping']

        return await ctx.reply(embed=success_embed(
            f"{EMOJIS['hu_peng']} Ghost ping detector",
            f"Ghost ping detector has now been **{'Enabled' if p else 'Disabled'}**"
        ))

    @commands.command(aliases=['antihoisting', 'nohoist'], help="Configure antihoisting for your server!")
    @commands.cooldown(3, 120, commands.BucketType.user)
    @commands.bot_has_permissions(manage_nicknames=True)
    @commands.has_permissions(manage_guild=True)
    async def antihoist(self, ctx):
        g = await self.client.get_guild_config(ctx.guild.id)
        g.update({"antihoisting": False if g['antihoisting'] else True})
        p = g['antihoisting']

        m = await ctx.reply(f"""
{EMOJIS['tick_yes']} Antihoisting has now been **{'Enabled' if p else 'Disabled'}**.
{EMOJIS['loading']+'Scanning current nicknames...' if p else ''}
                            """)
        i = 0
        i_ = 0
        i__ = 0

        if p:
            async with ctx.channel.typing():
                for member in ctx.guild.members:
                    if not member.bot:
                        if member.display_name[0] in ANTIHOIST_CHARS:
                            try:
                                await member.edit(nick="Moderated Nickname")
                                i += 1
                            except Exception:
                                i_ += 1
                            i__ += 1

            await m.edit(f"{EMOJIS['tick_yes']} Antihoisting has been enabled.\n\n{EMOJIS_FOR_COGS['info']}  I found `{i__}` hoisted nicknames.\n{EMOJIS['tick_yes']} I moderated `{i}` of them.\n{EMOJIS['tick_no']} I failed to moderate `{i_}` of them because of insufficient perms/role hierarchy.")

    @commands.command(
        help="Configure bump reminders for your server!",
        aliases=['bumpreminders', 'bumpremind', 'bumptime', 'br']
    )
    @commands.cooldown(3, 15, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def bumpreminder(self, ctx, choice=None, role: t.Union[discord.Role, str] = None):
        prefix = ctx.clean_prefix
        g = await self.client.get_guild_config(ctx.guild.id)
        enabled = True if g['bump_reminders'] else False

        yes = ['enable', 'yes', 'on', 'true']
        no = ['disable', 'no', 'off', 'false']

        em = success_embed(
            f"{EMOJIS['disboard']} Bump Reminders!",
            f"""
Bump reminders are currently **{'Enabled' if enabled else 'Disabled'}** for this server.

**Ping role:** {'None' if not enabled else "<@&"+str(g['bump_reminders']['role'])+">" if g['bump_reminders']['role'] is not None else "None"}
**Reward role:** {"None" if not enabled else "<@&"+str(g['bump_reminders'].get('reward'))+">" if g['bump_reminders'].get('reward') is not None else "None"}

**You can use the following commands to configure it!**

- `{prefix}bumpreminder enable/disable` - To enable/disable bumpreminders.
- `{prefix}bumpreminder role @role` - To set a reminder role when bumps are available.
- `{prefix}bumpreminder rewrad @role` - To set a reward role for bumpers.
            """
        ).set_thumbnail(url="https://cdn.discordapp.com/emojis/861565998510637107.png?v=1")

        if choice is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=em)
        if choice.lower() in yes:
            if enabled:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already enabled!",
                    "Bump reminders are already enabled for this server."
                ))
            g.update({
                "bump_reminders": {
                    "channel_id": None,
                    "time": None,
                    "bumper": None,
                    "role": None,
                    "reward": None
                }
            })
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['disboard']} Bump Reminders Enabled!",
                f"Bump reminders have been enabled!\n\nYou can also set a bump role using `{prefix}bumpreminder role @role`\nThis role will get pinged when a bump is available.\nAnd you can use `{prefix}bumpreminder reward @role` to reward a role to bumpers!"
            ).set_thumbnail(url="https://cdn.discordapp.com/emojis/861565998510637107.png?v=1"))
        if choice.lower() in no:
            if not enabled:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Already disabled!",
                    "Bump reminders are already disabled for this server."
                ))
            g.update({"bump_reminders": None})
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['disboard']} Bump Reminders Disabled!",
                "Bump reminders have been disabled."
            ))
        if choice.lower() == 'role':
            if not enabled:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Not enabled!",
                    "You need to enable bump reminders to configure the bump role."
                ))
            if role is None:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Usage!",
                    f"Please use `{prefix}bumpreminder role @role`"
                ))
            if isinstance(role, str) and role.lower() != 'none':
                ctx.command.reset_cooldown(ctx)
                raise commands.RoleNotFound(role)
            if isinstance(role, discord.Role):
                g['bump_reminders'].update({
                    "role": role.id
                })
                return await ctx.reply(embed=success_embed(
                    f"{EMOJIS['tick_yes']} Bump role updated!",
                    f"The role {role.mention} will be pinged when a bump is available."
                ))
            g['bump_reminders'].update({
                "role": None
            })
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Bump role removed!",
                "The role won't be pinged when a bump is available."
            ))
        if choice.lower() in ['reward', 'give']:
            if not enabled:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Not enabled!",
                    "You need to enable bump reminders to configure the reward role."
                ))
            if role is None:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Invalid Usage!",
                    f"Please use `{prefix}bumpreminder reward @role`"
                ))
            if isinstance(role, str) and role.lower() != 'none':
                ctx.command.reset_cooldown(ctx)
                raise commands.RoleNotFound(role)
            if isinstance(role, discord.Role):
                if role.position >= ctx.guild.me.top_role.position:
                    ctx.command.reset_cooldown(ctx)
                    return await ctx.reply(embed=error_embed(
                        f"{EMOJIS['tick_no']} Give me a higher role!",
                        f"I can't give roles higher than my top role ({ctx.guild.me.top_role.mention})."
                    ))
                g['bump_reminders'].update({
                    "reward": role.id
                })
                return await ctx.reply(embed=success_embed(
                    f"{EMOJIS['tick_yes']} Reward role updated!",
                    f"The role {role.mention} will be rewarded to bumpers!"
                ))
            g['bump_reminders'].update({
                "reward": None
            })
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Reward role removed!",
                "The role won't be given to bumpers."
            ))
        else:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=em)


def setup(client):
    client.add_cog(config(client))

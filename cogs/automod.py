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
import typing as t

from discord.ext import commands
from utils.bot import EpicBot
from config import BADGE_EMOJIS, EMOJIS, DEFAULT_AUTOMOD_CONFIG, DEFAULT_BANNED_WORDS
from utils.embed import success_embed, error_embed
from utils.converters import Lower
from utils.ui import Paginator


async def show_automod_config(client: EpicBot, ctx: commands.Context):
    g = await client.get_guild_config(ctx.guild.id)
    am = g['automod']
    tick_yes = EMOJIS['tick_yes']
    tick_no = EMOJIS['tick_no']

    cancer = ['ignored_channels', 'allowed_roles']

    embed1 = success_embed(
        "Automod Filters Configuration",
        "**Here are all the automod filters status:**"
    )
    embed2 = success_embed(
        "Automod Whitelist Configuration",
        "**Here are all the automod whitelist configuration:**"
    )

    for e in am:
        if e not in cancer:
            embed1.add_field(
                name = f"**{e.replace('_', ' ').title()}**",
                value = tick_yes+ ' Enabled' if am[e]['enabled'] else tick_no+ ' Disabled'
            )
        
    good_roles_msg = ""
    good_channels_msg = ""

    for r in am['allowed_roles']:
         good_roles_msg += f"<@&{r}> "
    for c in am['ignored_channels']:
        good_channels_msg += f"<#{c}> "

    embed2.add_field(name = "Whitelisted Roles:", value=good_roles_msg or 'None', inline=False)
    embed2.add_field(name="Whitelisted Channels:", value=good_channels_msg or 'None', inline=False)
    await ctx.reply(embed=embed1, view=AutomodConfigView(ctx=ctx, embeds=[embed1, embed2]))

async def am_badword_toggle(client: EpicBot, ctx: commands.Context, choice: Lower = None):
    prefix = ctx.clean_prefix
    g = await client.get_guild_config(ctx.guild.id)
    am = g['automod']
    enabled = True if am['banned_words']['enabled'] else False

    show_emb = success_embed(
        "Automod Bad Word Status",
        f"""
Automod bad words is currently {EMOJIS['tick_yes']+ ' Enabled' if enabled else EMOJIS['tick_no']+ ' Disabled'}

**You can use these commands to add/remove bad words:**

-`{prefix}automod badword add/remove` - To add/remove bad words.
-`{prefix}automod badword list` - To see a list of bad words.
        """
    )
    if not choice or choice not in ['enable', 'on', 'off', 'disable']:
        return await ctx.reply(embed=show_emb)

    if choice in ['on', 'enable']:
        if enabled:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Already Enabled!",
                "The automod bad word module is already enabled!"
            ))
        am['banned_words'].update({"enabled": True})
        return await ctx.reply(embed=success_embed(
            f"{EMOJIS['tick_yes']} Module Enabled!",
            f"The automod module `{choice}` has been **{EMOJIS['tick_yes']} Enabled!**\nYou can add bad word usign"
        ))
    else:
        if not enabled:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Already Disabled!",
                "The automod bad word module is already disabled!"
            ))
        am['banned_words'].update({"enabled": False})
        return await ctx.reply(embed=success_embed(
            f"{EMOJIS['tick_yes']} Module Disabled!",
            f"The automod module `{choice}` has been **{EMOJIS['tick_no']} Disabled!**"
        ))

async def am_add_badword(client: EpicBot, ctx: commands.Context, word: Lower = None):
    g = await client.get_guild_config(ctx.guild.id)
    am = g['automod']
    enabled = True if am['banned_words']['enabled'] else False

    if not enabled:
        return await ctx.reply(embed=error_embed(
            f"{EMOJIS['tick_no']} Not Enabled!",
            f"Please enable the automod `badword` module before using this command!\nEnable it by using `{ctx.clean_prefix}automod badword enable`"
        ))
    
    if word is None:
        return await ctx.reply(embed=error_embed(
            f"{EMOJIS['tick_no']} No Word!",
            "Please provide a word for me to add!"
        ))
    
    if word in DEFAULT_BANNED_WORDS:
        if word in am['banned_words']['removed_words']:
            am['banned_words']['removed_words'].remove(word)
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Bad Word Added!",
                f"The `{word}` word has been added into the bad word list!"
            ))
        else:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Bad Word Already Exist!",
                f"The `{word}` bad word is already added in the bad word list!"
            ))
        
    if word in am['banned_words']['words']:
        return await ctx.reply(embed=error_embed(
            f"{EMOJIS['tick_no']} Bad Word Already Exist!",
            f"The `{word}` bad word is already added in the bad word list!"
        ))
    else:
        am['banned_words']['words'].append(word)
        return await ctx.reply(embed=success_embed(
            f"{EMOJIS['tick_yes']} Bad Word Added!",
            f"The `{word}` word has been added into the bad word list!"
        ))

async def am_remove_badword(client: EpicBot, ctx: commands.Context, word: Lower = None):
    g = await client.get_guild_config(ctx.guild.id)
    am = g['automod']
    enabled = True if am['banned_words']['enabled'] else False

    if not enabled:
        return await ctx.reply(embed=error_embed(
            f"{EMOJIS['tick_no']} Not Enabled!",
            f"Please enable the automod `badword` module before using this command!\nEnable it by using `{ctx.clean_prefix}automod badword enable`"
        ))
    
    if word is None:
        return await ctx.reply(embed=error_embed(
            f"{EMOJIS['tick_no']} No Word!",
            "Please provide a word for me to add!"
        ))
    
    if word in DEFAULT_BANNED_WORDS:
        if word not in am['banned_words']['removed_words']:
            am['banned_words']['removed_words'].add(word)
            return await ctx.reply(embed=success_embed(
                f"{EMOJIS['tick_yes']} Bad Word Removed!",
                f"The `{word}` word has been removed from the bad word list!"
            ))
        else:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Bad Word Not Exist!",
                f"The `{word}` word is not in the bad word list!!"
            ))

        
    if word not in am['banned_words']['words']:
        return await ctx.reply(embed=error_embed(
            f"{EMOJIS['tick_no']} Bad Word Not Found!",
            f"The `{word}` word is not a bad word!"
        ))
    else:
        am['banned_words']['words'].remove(word)
        return await ctx.reply(embed=success_embed(
            f"{EMOJIS['tick_yes']} Bad Word Removed!",
            f"The `{word}` word has been removed from the bad word list!"
        ))

async def view_badword_list(client: EpicBot, ctx: commands.Context):
    g = await client.get_guild_config(ctx.guild.id)
    am = g['automod']
    enabled = True if am['banned_words']['enabled'] else False

    if not enabled:
        return await ctx.reply(embed=error_embed(
            f"{EMOJIS['tick_no']} Not Enabled!",
            f"Please enable the automod `badword` module before using this command!\nEnable it by using `{ctx.clean_prefix}automod badword enable`"
        ))
    paginator = commands.Paginator(prefix="", suffix="", max_size=500)
    banned_list = []
    all_embeds = []

    for wrd in DEFAULT_BANNED_WORDS:
        if wrd.lower() not in am['banned_words']['removed_words']:
            banned_list.append(wrd.lower())

    for word in am['banned_words']['words']:
        banned_list.append(word.lower())
    
    i = 1
    for badword in banned_list:
        paginator.add_line(f"{i} - `{badword}`")
        i += 1
    
    for page in paginator.pages:
        all_embeds.append(success_embed(
            "All Bad Words",
            page
        ))
    
    if len(all_embeds) == 1:
        return await ctx.author.send(embed=all_embeds[0])
    view = Paginator(ctx, all_embeds)
    await ctx.author.send(embed=all_embeds[0], view=view)

class AutomodConfigView(discord.ui.View):
    def __init__(self, ctx: commands.Context, embeds: list):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.embeds = embeds

    @discord.ui.button(label="Filters Config", style=discord.ButtonStyle.blurple)
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


class automod(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client

    @commands.group(name='automod', aliases=['am'], help = "Configure automod for your server!")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(administrator=True)
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def _automod(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(ctx.command)
        
    @_automod.command(name='show', help = 'Get the current automod configuration.')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _show(self, ctx: commands.Context):
        await show_automod_config(self.client, ctx)
        
    @_automod.group(name='badwords', aliases=['badword'], help = "Enable/Disable badwords automod for your server!", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def automod_badword(self, ctx: commands.Context, choice: Lower = None):
        await am_badword_toggle(self.client, ctx, choice)

    @automod_badword.command(name='add', help = "Add a bad word to the list!")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(2, 20, commands.BucketType.user)
    async def am_badword_add(self, ctx: commands.Context, *,word: Lower = None):
        await am_add_badword(self.client, ctx, word)

    @automod_badword.command(name='remove', help = "Remove a bad word from the list!")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(2, 20, commands.BucketType.user)
    async def am_badword_remove(self, ctx: commands.Context, *,word: Lower = None):
        await am_remove_badword(self.client, ctx, word)

    @automod_badword.command(name='list', aliases=['show', 'l'], help = "View the list of bad words!")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(2, 20, commands.BucketType.user)
    async def am_badword_list(self, ctx: commands.Context):
        await view_badword_list(self.client, ctx)

    
    @_automod.command(name='roles', aliases=['role'], help = "Add/Remove a role from whitelist")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(2, 20, commands.BucketType.user)
    async def am_role_whitelist(self, ctx: commands.Context, choice: Lower = None):
        pass #best thing existed in python


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


def setup(client: EpicBot):
    client.add_cog(automod(client))

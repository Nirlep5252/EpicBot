import json
import discord
from discord.ext import commands
from typing import Dict, List
from utils.bot import EpicBot
from utils.embed import error_embed, success_embed, process_embeds_from_json
from utils.message import wait_for_msg
from utils.ui import Confirm, Paginator
from utils.converters import Lower
from config import PREMIUM_GUILDS, EMOJIS, SUPPORT_SERVER_LINK, custom_cmds_tags_lemao


class CCEditView(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.value = None

    @property
    def embed(self) -> discord.Embed:
        return success_embed(
            f"{EMOJIS['settings_color']} Editing custom command...",
            "Please select what you want to edit, by clicking one of the buttons!"
        )

    @discord.ui.button(label='Name', style=discord.ButtonStyle.blurple)
    async def name(self, b: discord.ui.Button, i: discord.Interaction):
        self.value = 'name'
        self.stop()

    @discord.ui.button(label='Description', style=discord.ButtonStyle.blurple)
    async def description(self, b: discord.ui.Button, i: discord.Interaction):
        self.value = 'desc'
        self.stop()

    @discord.ui.button(label='Reply', style=discord.ButtonStyle.blurple)
    async def reply(self, b: discord.ui.Button, i: discord.Interaction):
        self.value = 'reply'
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.danger)
    async def cancel(self, b: discord.ui.Button, i: discord.Interaction):
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.ctx.author.id == interaction.author.id:
            return True
        await interaction.response.send_message(f"This is {self.ctx.author.mention}'s view, not yours.", ephemeral=True)


class custom(commands.Cog, description="Custom commands, custom responses and more!"):
    def __init__(self, client: EpicBot):
        self.client = client

    async def check_if_embed_is_shit_or_not_lmfao(self, ctx: commands.Context, temp_msg_cont, main_msg) -> bool:
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

            helpful_text = ""
            if test == 'pain author name':
                helpful_text = "**Your embed is missing a `name` value inside of the `author` value.**"
            elif test == 'pain footer text':
                helpful_text = "**Your embed is missing a `text` value inside of the `footer` value.**"
            elif test == 'pain empty fields':
                helpful_text = "**Your fields are incomplete one of them either has a value of `""` or is missing a value completely.**"
            elif test == 'pain invalid urls':
                helpful_text = "**One of your URLs is invalid and isn't a proper URL.**\nPlease make you enter proper URLs using `http` or `https`."
            elif test == 'pain empty embed':
                helpful_text = "**Your embed is empty.**\nPlease make sure you have atleast a title/description/field."
            else:
                return True
            await main_msg.edit(embed=error_embed(
                f"{EMOJIS['tick_no']} Incomplete Embed!",
                f"{helpful_text}\n{make_sure_ur_embed_is_not_a_piece_of_shit}"
            ).set_footer(text="Please re-run the command."))
            return False
        except Exception:
            await main_msg.edit(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Embed Response!",
                "Please go to https://embedbuilder.nadekobot.me/ and paste a valid embed code next time!\nPlease re-run the command."
            ).set_image(url="https://i.imgur.com/HrjySSB.png"))
            return False

    @commands.group(aliases=['cc', 'customcmd'], help="Configure custom commands for your server!")
    @commands.cooldown(6, 10, commands.BucketType.user)
    async def customcommand(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(ctx.command)

    @customcommand.command(name="show", aliases=['list'], help="Show the list of all the custom commands.")
    @commands.cooldown(6, 10, commands.BucketType.user)
    async def cc_show(self, ctx: commands.Context):
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

    @customcommand.command(name='create', aliases=['add'], help="Create a custom command!")
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def cc_create(self, ctx: commands.Context):
        cc_limit = 25
        prefix = ctx.clean_prefix
        g = await self.client.get_guild_config(ctx.guild.id)
        if "custom_cmds" not in g:
            g.update({"custom_cmds": []})
        custom_cmds_list: List[Dict[str, str]] = g["custom_cmds"]
        custom_cmds_names = [c['name'] for c in custom_cmds_list]
        if len(custom_cmds_list) >= cc_limit and ctx.guild.id not in PREMIUM_GUILDS:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Too many commands!",
                f"The maximum limit for custom commands is **{cc_limit}**.\nPlease delete some commands to create more."
            ))
        final = {}

        # Getting the command name
        main_msg = await ctx.reply(embed=success_embed(
            f"{EMOJIS['loading']} Custom command process",
            "Please enter a name for your command..."
        ))
        name_msg = await wait_for_msg(ctx, 60, main_msg)
        if name_msg == 'pain':
            return
        name = name_msg.content.lower().replace(" ", "_")
        actual_cmd = self.client.get_command(name)
        if name in custom_cmds_names or actual_cmd is not None:
            ctx.command.reset_cooldown(ctx)
            return await main_msg.edit(embed=error_embed(
                f"{EMOJIS['tick_no']} Already Exists!",
                f"A command named `{name}` already exists.\nPlease re-run the command."
            ))
        if len(name) > 25:
            ctx.command.reset_cooldown(ctx)
            return await main_msg.edit(embed=error_embed(
                f"{EMOJIS['tick_no']} Too long!",
                "The command name can't be longer than **25** characters."
            ))
        final['name'] = name

        # Getting the command description
        await main_msg.edit(embed=success_embed(
            f"{EMOJIS['loading']} Custom command process",
            "Please enter a description for your command..."
        ))
        desc_msg = await wait_for_msg(ctx, 60, main_msg)
        if desc_msg == 'pain':
            return
        desc = desc_msg.content
        desc_limit = 250
        if len(desc) > desc_limit:
            return await main_msg.edit(embed=error_embed(
                f"{EMOJIS['tick_no']} Too long!",
                f"The command description can't be longer than **{desc_limit}** characters."
            ))
        final['desc'] = desc

        # Checking if they want it as an embed or not
        view = Confirm(ctx, 60)
        await main_msg.edit(embed=success_embed(
            f"{EMOJIS['loading']} Custom command process",
            "Do you want your command response to be an embed?\nClick `No` if you are confused."
        ), view=view)
        await view.wait()
        if view.value is None:
            ctx.command.reset_cooldown(ctx)
            return await main_msg.edit(embed=error_embed(
                f"{EMOJIS['tick_no']} Too late!",
                "Looks like you didn't respond in time...\nPlease re-run the command."
            ), view=None)
        final['embed'] = view.value

        # Getting the command response
        for_embed_users_nerds = "\nGo to https://embedbuilder.nadekobot.me/ and paste the generated embed code here!\n"
        reeee = success_embed(
            f"{EMOJIS['loading']} Custom command process",
            f"Please type the response for your command here!{for_embed_users_nerds if view.value  else ''}\nHere are the tags that you can use in custom commands:\n{custom_cmds_tags_lemao}"
        ).set_footer(text="Please reply within 10 mins.")
        if view.value:
            reeee.set_image(url="https://i.imgur.com/HrjySSB.png")
        await main_msg.edit(embed=reeee, view=None)
        response_msg = await wait_for_msg(ctx, 600, main_msg)
        if response_msg == 'pain':
            return
        response = response_msg.content
        if view.value:
            interesting = await self.check_if_embed_is_shit_or_not_lmfao(ctx, response, main_msg)
            if not interesting:
                return
        final['reply'] = response
        custom_cmds_list.append(final)
        return await main_msg.edit(embed=success_embed(
            f"{EMOJIS['settings_color']} Custom Command Added!",
            f"The custom command with the name `{final['name']}` has been added.\nYou can use `{prefix}cc show` to see the list of all custom commands"
        ))

    @customcommand.command(name='edit', aliases=['update'], help="Edit a custom command!")
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def cc_edit(self, ctx: commands.Context, name: Lower = None):
        prefix = ctx.clean_prefix
        if name is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter a command name to edit.\nCorrect Usage: `{prefix}cc edit <name>`\nExample: `{prefix}cc edit uwu`"
            ))
        g = await self.client.get_guild_config(ctx.guild.id)
        if "custom_cmds" not in g:
            g.update({"custom_cmds": []})
        custom_cmds_list: List[Dict[str, str]] = g["custom_cmds"]
        custom_cmds_names = [c['name'] for c in custom_cmds_list]
        if name not in custom_cmds_names:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Not Found!",
                f"Custom command named `{name}` does not exist.\nPlease use `{prefix}cc list` to get the list of all custom commands."
            ))
        view = CCEditView(ctx)
        main_msg = await ctx.reply(embed=view.embed, view=view)
        await view.wait()
        if not view.value:
            return await main_msg.edit(f"{EMOJIS['tick_no']}Command cancelled.")
        await main_msg.edit(embed=success_embed(
            f"Editing {view.value.title()}",
            f"Please enter a new {view.value} for {name}" + (f"\nHere are the tags that you can use in custom commands:\n{custom_cmds_tags_lemao}" if view.value == 'reply' else '')
        ), view=None)
        temp = await wait_for_msg(ctx, 600 if view.value == 'reply' else 60, main_msg)
        if temp == 'pain':
            return
        final = temp.content
        current_command = [c for c in custom_cmds_list if c['name'] == name][0]
        if current_command['embed'] and view.value == 'reply':
            interesting = await self.check_if_embed_is_shit_or_not_lmfao(ctx, final, main_msg)
            if not interesting:
                return
        if view.value == 'name':
            final = final.replace(' ', '_')
        custom_cmds_list.remove(current_command)
        current_command[view.value] = final
        custom_cmds_list.append(current_command)
        return await main_msg.edit(embed=success_embed(
            f"{EMOJIS['tick_yes']} Custom command edited!",
            f"Your custom command has been edited!\nYou can check the updated verion using `{prefix}{name if view.value != 'name' else final}`."
        ))

    @customcommand.command(name='delete', aliases=['remove'], help="Delete a custom command!")
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.max_concurrency(1, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def cc_delete(self, ctx: commands.Context, name: Lower = None):
        prefix = ctx.clean_prefix
        if name is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter a command name to delete.\nCorrect Usage: `{prefix}cc delete <name>`\nExample: `{prefix}cc delete uwu`"
            ))
        g = await self.client.get_guild_config(ctx.guild.id)
        if "custom_cmds" not in g:
            g.update({"custom_cmds": []})
        custom_cmds_list: List[Dict[str, str]] = g["custom_cmds"]
        custom_cmds_names = [c['name'] for c in custom_cmds_list]
        if name not in custom_cmds_names:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Not Found!",
                f"Custom command named `{name}` does not exist.\nPlease use `{prefix}cc list` to get the list of all custom commands."
            ))
        view = Confirm(ctx, 60)
        main_msg = await ctx.reply(f"Are you sure you want to delete `{name}`?", view=view)
        await view.wait()
        if view.value is None:
            ctx.command.reset_cooldown(ctx)
            return await main_msg.edit(content="You didn't respond in time.", view=None)
        if not view.value:
            ctx.command.reset_cooldown(ctx)
            return await main_msg.edit(content="Cancelled.", view=None)
        for e in custom_cmds_list:
            if e['name'] == name:
                custom_cmds_list.remove(e)
        return await main_msg.edit(content=f"The custom command named `{name}` has been deleted.", view=None)

    @customcommand.command(name='tags', help="View all the custom command tags!")
    @commands.cooldown(5, 60, commands.BucketType.user)
    @commands.max_concurrency(1, commands.BucketType.user)
    async def cc_tags(self, ctx: commands.Context):
        return await ctx.reply(embed=success_embed(
            f"{EMOJIS['settings_color']} Tags for custom commands!",
            f"Here are the tags you can use for custom commands: \n{custom_cmds_tags_lemao}"
        ))


def setup(client):
    client.add_cog(custom(client))

import discord.ui
from discord.ext import commands
from utils.bot import EpicBot
from utils.constants import DEFAULT_YOUTUBE_MSG, YOUTUBE_TAGS
from utils.custom_checks import coming_soon
from utils.embed import success_embed, error_embed
from utils.message import wait_for_msg
from utils.ui import Confirm
from config import EMOJIS, DEFAULT_TWITCH_MSG
from cogs_hidden.youtube import get_yt_channel, check_new_video


class TwitchEditView(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="Streamer", custom_id='streamer', style=discord.ButtonStyle.blurple)
    async def streamer(self, button, interaction):
        self.value = 'username'
        self.stop()

    @discord.ui.button(label="Discord Channel", custom_id='channel', style=discord.ButtonStyle.blurple)
    async def channel(self, button, interaction):
        self.value = 'channel_id'
        self.stop()

    @discord.ui.button(label="Message", custom_id='message', style=discord.ButtonStyle.blurple)
    async def message(self, button, interaction):
        self.value = 'message'
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, button, interaction):
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id == self.ctx.author.id:
            return True
        return await interaction.response.send_message("This isn't your command!", ephemeral=True)


class YouTubeEditView(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="YouTube Channel", custom_id='youtube_id', style=discord.ButtonStyle.blurple)
    async def streamer(self, button, interaction):
        self.value = 'youtube_id'
        self.stop()

    @discord.ui.button(label="Discord Channel", custom_id='channel_id', style=discord.ButtonStyle.blurple)
    async def channel(self, button, interaction):
        self.value = 'channel_id'
        self.stop()

    @discord.ui.button(label="Message", custom_id='message', style=discord.ButtonStyle.blurple)
    async def message(self, button, interaction):
        self.value = 'message'
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, button, interaction):
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id == self.ctx.author.id:
            return True
        return await interaction.response.send_message("This isn't your command!", ephemeral=True)


class notifications(commands.Cog, description="All the commands related to notifications! 👀"):
    def __init__(self, client: EpicBot):
        self.client = client

    @commands.group(aliases=['twitchnotification', 'twitch-notification', 'twitchnotif'], help="Configure Twitch notifications for your server.")
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def twitch(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(ctx.command)

    @twitch.command(name="show", help="Get the current Twitch configuration")
    async def twitch_show(self, ctx: commands.Context):
        notset = '❌ Not Set'
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        twitch_config = guild_config['twitch']
        if 'message' not in twitch_config or 'currently_live' not in twitch_config:
            twitch_config.update({"message": None, "currently_live": False})
        embed = success_embed(
            f"{EMOJIS['twitch']} Twitch Configuration!",
            "Here is your current twitch configuration:"
        )
        embed.add_field(
            name="Streamer:",
            value=f"[{twitch_config['username']}](https://twitch.tv/{twitch_config['username']})" if twitch_config['username'] is not None else notset,
            inline=True
        )
        embed.add_field(name="Channel:", value=notset if twitch_config['channel_id'] is None else '<#'+str(twitch_config['channel_id'])+'>', inline=True)
        embed.add_field(name="Message:", value=f"```{DEFAULT_TWITCH_MSG if twitch_config['message'] is None else twitch_config['message']}```", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/775735414362734622/852899330464415754/twitch_logo.png")
        return await ctx.reply(embed=embed)

    @twitch.command(name="enable", help="Enable Twitch configuration for your server!")
    @commands.has_permissions(manage_guild=True)
    async def twitch_enable(self, ctx: commands.Context):
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        twitch_config = guild_config['twitch']
        enabled = False if twitch_config['channel_id'] is None else True
        if enabled:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Already enabled!",
                f"Looks like twitch notifications are already enabled!\nPlease use `{ctx.clean_prefix}twitch show` to get the current configuration."
            ))
        main_msg = await ctx.reply(embed=success_embed(
            f"{EMOJIS['twitch']} Twitch configuration: 1/2",
            "Please enter the streamer username to continue..."
        ))
        msg_streamer = await wait_for_msg(ctx, 60, main_msg)
        if msg_streamer == 'pain':
            return
        twitch_config.update({"username": msg_streamer.content.lower()})
        await main_msg.edit(embed=success_embed(
            f"{EMOJIS['twitch']} Twitch configuration: 2/2",
            "Enter the channel where you want the live notification to go."
        ))
        msg_channel = await wait_for_msg(ctx, 60, main_msg)
        if msg_channel == 'pain':
            return
        try:
            twitch_channel = await commands.TextChannelConverter().convert(ctx, msg_channel.content)
        except commands.ChannelNotFound:
            await main_msg.delete()
            raise commands.ChannelNotFound(msg_channel.content)
        twitch_config.update({"channel_id": twitch_channel.id})
        return await main_msg.edit(embed=success_embed(
            f"{EMOJIS['twitch']} Twitch notifications setup!",
            f"The twitch notifications have been set to channel {twitch_channel.mention}.\nTo edit the live message you can use `{ctx.clean_prefix}twitch edit`"
        ))

    @twitch.command(name="disable", help="Disable Twitch notifications in your server.")
    @commands.has_permissions(manage_guild=True)
    async def twitch_disable(self, ctx: commands.Context):
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        twitch_config = guild_config['twitch']
        enabled = False if twitch_config['channel_id'] is None else True
        if not enabled:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(f"{EMOJIS['tick_no']}Twitch notifications are not disabled.")
        twitch_config.update({
            "channel_id": None,
            "username": None,
            "message": None,
            "currently_live": False
        })
        return await ctx.reply(embed=success_embed(
            f"{EMOJIS['twitch']} Disabled!",
            "The twitch live notifications have been disabled!"
        ))

    @twitch.command(name="edit", help="Edit your Twitch configuration.")
    @commands.has_permissions(manage_guild=True)
    async def twitch_edit(self, ctx: commands.Context):
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        twitch_config = guild_config['twitch']
        enabled = False if twitch_config['channel_id'] is None else True
        if 'message' not in twitch_config or 'currently_live' not in twitch_config:
            twitch_config.update({"message": None, "currently_live": False})
        if not enabled:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(f"{EMOJIS['tick_no']}You need to enable twitch notifications to run this command.\nPlease use `{ctx.clean_prefix}twitch enable` to enable them.")
        view = TwitchEditView(ctx)
        main_msg = await ctx.reply(embed=success_embed(
            f"{EMOJIS['twitch']} Editing twitch config",
            "Please select what you want to edit, by clicking one of the buttons!"
        ), view=view)
        await view.wait()
        if not view.value:
            return await main_msg.edit(content="Command cancelled or timed out!", embed=None, view=None)
        embed = success_embed(
            f"{EMOJIS['twitch']} Editing {view.value.replace('_id', '').title()}",
            f"Your current value is: {'```' if view.value != 'channel_id' else '<#'}{twitch_config[view.value] or DEFAULT_TWITCH_MSG}{'```' if view.value != 'channel_id' else '>'}\n\nPlease send a message to edit this within 60 seconds!\nYou can send `cancel` to cancel this."
        )
        if view.value == 'message':
            embed.add_field(
                name="Here are the tags that you can use:",
                value="`{streamer}` - The username of the streamer.\n`{url}` - The twitch link to the stream."
            )
        await main_msg.edit(embed=embed, view=None)
        m = await wait_for_msg(ctx, 60, main_msg)
        if m == 'pain':
            return
        final = None
        if view.value == 'channel_id':
            try:
                channel = await commands.TextChannelConverter().convert(ctx, m.content)
                final = channel.id
            except Exception:
                await main_msg.delete()
                raise commands.ChannelNotFound(m.content)
        final = final or m.content
        twitch_config.update({view.value: final})
        return await main_msg.edit(embed=success_embed(
            f"{EMOJIS['twitch']} The twitch {view.value.replace('_id', '')} has successfully been edited!",
            f"You can use `{ctx.clean_prefix}twitch show` to see your current configuration."
        ))

    @commands.group(aliases=['yt', 'ytnotif', 'youtub', 'youtubee'], help="Commands related to YouTube.")
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def youtube(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(ctx.command)

    @youtube.command(name="show", help="Get the current YouTube configuration.")
    async def yt_show(self, ctx: commands.Context):
        notset = '❌ Not Set'
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        yt_config = guild_config['youtube']
        yt_channel = await get_yt_channel(self.client, yt_config['youtube_id'])
        embed = success_embed(
            f"{EMOJIS['youtube']} YouTube Configuration!",
            "Here are your current settings:"
        )
        embed.add_field(
            name="YouTube Channel:",
            value=f"[{'404 Channel Not Found' if yt_channel is None else yt_channel.snippet.title}](https://youtube.com/channel/{yt_config['youtube_id']})" if yt_config['youtube_id'] is not None else notset,
            inline=True
        )
        embed.add_field(
            name="Notification Channel:",
            value=notset if yt_config['channel_id'] is None else '<#'+str(yt_config['channel_id'])+'>',
            inline=True
        )
        embed.add_field(name="Message:", value=f"```{yt_config.get('message') or DEFAULT_YOUTUBE_MSG}```", inline=False)
        embed.set_thumbnail(url="https://gizblog.it/wp-content/uploads/2017/08/youtube-logo-nuovo-banner.jpg")
        return await ctx.reply(embed=embed)

    @youtube.command(name="enable", help="Enable YouTube notifications in your server!")
    @commands.has_permissions(manage_guild=True)
    async def yt_enable(self, ctx: commands.Context):
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        yt_config = guild_config['youtube']
        enabled = False if yt_config['channel_id'] is None else True
        if enabled:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Already enabled!",
                f"Looks like YouTube notifications are already enabled!\nPlease use `{ctx.clean_prefix}youtube show` to get the current configuration."
            ))
        main_msg = await ctx.reply(embed=success_embed(
            f"{EMOJIS['youtube']} YouTube configuration: 1/2",
            "Please enter the YouTuber channel ID to continue..."
        ).set_image(url="https://cdn.discordapp.com/attachments/859335247547990026/884661479717105674/unknown.png"))
        msg_ytber = await wait_for_msg(ctx, 60, main_msg)
        if msg_ytber == 'pain':
            return
        yt_channel = await get_yt_channel(self.client, msg_ytber.content)
        if yt_channel is None:
            ctx.command.reset_cooldown(ctx)
            return await main_msg.edit(embed=error_embed(
                f"{EMOJIS['tick_no']} YouTube channel not found!",
                "Make sure you entered the correct YouTube channel ID"
            ).set_image(url="https://cdn.discordapp.com/attachments/859335247547990026/884661479717105674/unknown.png"))
        new_video = await check_new_video(self.client, yt_channel.id)
        view = Confirm(ctx)
        confirm_embed = success_embed(
            f"{EMOJIS['youtube']} Is this your requested YouTube channel?",
            f"""
**Channel:** [{yt_channel.snippet.title}](https://youtube.com/channel/{yt_channel.id})
**Description:** {yt_channel.snippet.description}
**Subs:** {yt_channel.statistics.subscriberCount}
**Views:** {yt_channel.statistics.viewCount}
            """
        )
        try:
            confirm_embed.set_thumbnail(url=yt_channel.snippet.thumbnails.default.url)
        except Exception:
            pass
        await main_msg.edit(embed=confirm_embed, view=view)
        await view.wait()
        if not view.value:
            ctx.command.reset_cooldown(ctx)
            return await main_msg.edit(content="Command cancelled or timed out.", embed=None, view=None)
        yt_config.update({"youtube_id": yt_channel.id, "last_vid": new_video.id})
        await main_msg.edit(embed=success_embed(
            f"{EMOJIS['youtube']} YouTube configuration: 2/2",
            "Enter the channel where you want the video notifications to go."
        ), view=None)
        msg_channel = await wait_for_msg(ctx, 60, main_msg)
        if msg_channel == 'pain':
            return
        try:
            final_channel = await commands.TextChannelConverter().convert(ctx, msg_channel.content)
        except commands.ChannelNotFound:
            await main_msg.delete()
            raise commands.ChannelNotFound(msg_channel.content)
        yt_config.update({"channel_id": final_channel.id})
        return await main_msg.edit(embed=success_embed(
            f"{EMOJIS['youtube']} YouTube notifications setup complete!",
            f"The YouTube notifications have been set to channel {final_channel.mention}.\nTo edit the video message you can use `{ctx.clean_prefix}youtube edit`"
        ))

    @youtube.command(name="disable", help="Disable YouTube notifications in your server.")
    @commands.has_permissions(manage_guild=True)
    async def yt_disable(self, ctx: commands.Context):
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        yt_config = guild_config['youtube']
        enabled = False if yt_config['channel_id'] is None else True
        if not enabled:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Already disabled!",
                f"YouTube notifications are already disabled!\nPlease use `{ctx.clean_prefix}youtube enable` to enable them."
            ))
        yt_config.update({'channel_id': None, 'youtube_id': None})
        return await ctx.reply(embed=success_embed(
            f"{EMOJIS['youtube']} YouTube Notifications disabled!",
            f"You can reenable them using `{ctx.clean_prefix}youtube enable`"
        ))

    @youtube.command(name="edit", help="Edit your YouTube configuration.")
    @commands.has_permissions(manage_guild=True)
    async def yt_edit(self, ctx: commands.Context):
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        yt_config = guild_config['youtube']
        enabled = False if yt_config['channel_id'] is None else True
        if not enabled:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(f"{EMOJIS['tick_no']}You need to enable YouTube notifications to run this command.\nPlease use `{ctx.clean_prefix}youtube enable` to enable them.")
        view = YouTubeEditView(ctx)
        main_msg = await ctx.reply(embed=success_embed(
            f"{EMOJIS['youtube']} Editing YouTube config",
            "Please select what you want to edit, by clicking one of the buttons!"
        ), view=view)
        await view.wait()
        if not view.value:
            return await main_msg.edit(content="Command cancelled or timed out!", embed=None, view=None)
        if view.value == 'channel_id':
            current = f"<#{yt_config['channel_id']}>"
        elif view.value == 'youtube_id':
            channel = await get_yt_channel(self.client, yt_config['youtube_id'])
            current = f"[{'404 Channel Not Found' if not channel else channel.snippet.title}](https://youtube.com/channel/{yt_config['youtube_id']})"
        else:
            current = f"```{yt_config[view.value] or DEFAULT_YOUTUBE_MSG}```"
        what_edit = view.value.replace('_id', '').replace('channel', 'discord channel').replace('youtube', 'youtube channel').title()
        embed = success_embed(
            f"{EMOJIS['youtube']} Editing {what_edit}",
            f"Your current value is: {current}\n\nPlease send a message to edit this within 60 seconds!\nYou can send `cancel` to cancel this."
        )
        if view.value == 'message':
            embed.add_field(
                name="Here are the tags that you can use:",
                value="\n".join(f"`{tag}` - {desc}" for tag, desc in YOUTUBE_TAGS.items())
            )
        if view.value == 'youtube_id':
            embed.set_image(url="https://cdn.discordapp.com/attachments/859335247547990026/884661479717105674/unknown.png")
        await main_msg.edit(embed=embed, view=None)
        m = await wait_for_msg(ctx, 60, main_msg)
        if m == 'pain':
            return
        final = None
        if view.value == 'channel_id':
            try:
                channel = await commands.TextChannelConverter().convert(ctx, m.content)
                final = channel.id
            except Exception:
                await main_msg.delete()
                raise commands.ChannelNotFound(m.content)
        elif view.value == 'youtube_id':
            temp_channel = await get_yt_channel(self.client, m.content)
            if temp_channel is None:
                ctx.command.reset_cooldown(ctx)
                return await main_msg.edit(embed=error_embed(
                    f"{EMOJIS['tick_no']} YouTube channel not found!",
                    "Please make sure you enter the correct channel ID next time.\nPlease re-run the command to try again."
                ).set_image(url="https://cdn.discordapp.com/attachments/859335247547990026/884661479717105674/unknown.png"), view=None)
            final = temp_channel.id
            new_video = await check_new_video(self.client, final)
            yt_config.update({"last_vid": new_video.id})
        final = final or m.content
        yt_config.update({view.value: final})
        return await main_msg.edit(embed=success_embed(
            f"{EMOJIS['youtube']} The {what_edit} has successfully been edited!",
            f"You can use `{ctx.clean_prefix}youtube show` to see your current configuration."
        ))


def setup(client: EpicBot):
    client.add_cog(notifications(client))

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
import DiscordUtils
import humanfriendly

from discord.ext import commands
from config import EMOJIS, MAIN_COLOR
from utils.embed import success_embed
from datetime import datetime
from DiscordUtils.Music import MusicPlayer
from utils.ui import Paginator
from utils.bot import EpicBot

music_ = DiscordUtils.Music()

# i wrote this cog while sleeping
# dont ask


class music(commands.Cog, description="Jam to some awesome tunes! 🎶"):
    def __init__(self, client: EpicBot):
        self.client = client
        self.skip_votes = {}

    def error_msg(self, error) -> str:
        if error == 'not_in_voice_channel':
            return f"{EMOJIS['tick_no']}You need to join a voice channel first."
        elif error == 'not_in_same_vc':
            return f"{EMOJIS['tick_no']}You need to be in the same voice channel as me."
        else:
            return "An error occured ._."

    def now_playing_embed(self, ctx, song) -> discord.Embed:
        return discord.Embed(
            title=song.title,
            url=song.url,
            color=MAIN_COLOR,
            timestamp=datetime.utcnow(),
            description=f"""
**Duration:** {humanfriendly.format_timespan(song.duration)}
**Channel:** [{song.channel}]({song.channel_url})
                        """
        ).set_image(url=song.thumbnail
        ).set_footer(text=f"Loop: {'✅' if song.is_looping else '❌'}", icon_url=ctx.guild.icon.url if ctx.guild.icon is not None else 'https://cdn.discordapp.com/embed/avatars/1.png'
        ).set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)

    @commands.command(help="I will join your voice channel.", aliases=['connect'])
    @commands.cooldown(3, 5, commands.BucketType.user)
    async def join(self, ctx: commands.Context):
        if not ctx.author.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg('not_in_voice_channel'))
        if ctx.guild.me.voice and len(ctx.guild.me.voice.channel.members) > 1:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("Someone else is already using the bot :c")
        try:
            await ctx.author.voice.channel.connect()
            await ctx.message.add_reaction('✅')
        except Exception as e:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(
                f"I wasn't able to connect to your voice channel.\nPlease make sure I have enough permissions.\nError: {e}"
            )

    @commands.command(help="I will leave your voice channel :c", aliases=['dc', 'disconnect'])
    @commands.cooldown(3, 5, commands.BucketType.user)
    async def leave(self, ctx: commands.Context):
        if not ctx.author.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg('not_in_voice_channel'))
        if not ctx.guild.me.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("I am not in a voice channel ._.")
        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg("not_in_same_vc"))
        player = music_.get_player(guild_id=ctx.guild.id)
        if player:
            try:
                await player.stop()
                await player.delete()
            except Exception:
                pass
        await ctx.voice_client.disconnect()
        await ctx.message.add_reaction('👋')

    @commands.command(help="V I B E and play epik music!!!", aliases=['p'])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def play(self, ctx, *, song_=None):
        if song_ is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(f"Correct Usage: `{ctx.clean_prefix}play <song/url>`\nExample: `{ctx.clean_prefix}play Rick Roll`")
        if not ctx.author.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg('not_in_voice_channel'))
        if not ctx.guild.me.voice:
            await ctx.invoke(self.client.get_command('join'))
        player = music_.get_player(guild_id=ctx.guild.id)
        if not player:
            player = music_.create_player(ctx, ffmpeg_error_betterfix=True)
        if not ctx.voice_client.is_playing():
            try:
                await player.queue(song_, search=True, bettersearch=True)
            except Exception:
                await player.queue(song_, search=True)
            song = await player.play()
            await ctx.send(embed=self.now_playing_embed(ctx, song))
        else:
            try:
                song = await player.queue(song_, search=True, bettersearch=True)
            except Exception:
                song = await player.queue(song_, search=True)
            await ctx.send(embed=discord.Embed(
                title=song.title,
                url=song.url,
                color=MAIN_COLOR,
                description=f"""
**Duration:** {humanfriendly.format_timespan(song.duration)}
**Channel:** [{song.channel}]({song.channel_url})
                            """
            ).set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url
            ).set_thumbnail(url=song.thumbnail
            ).set_footer(text=f"Song added to queue | Loop: {'✅' if song.is_looping else '❌'}", icon_url=ctx.guild.icon.url if ctx.guild.icon is not None else 'https://cdn.discordapp.com/embed/avatars/1.png'))

    @commands.command(help="Check the current playing song.", aliases=['np'])
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def nowplaying(self, ctx):
        player = music_.get_player(guild_id=ctx.guild.id)
        if not player:
            return await ctx.reply("Nothing is playing rn.")
        if not ctx.voice_client.is_playing():
            return await ctx.reply("No music playing rn ._.")
        song = player.now_playing()
        await ctx.reply(embed=self.now_playing_embed(ctx, song))

    @commands.command(help="Pause the song.")
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def pause(self, ctx):
        if not ctx.author.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg('not_in_voice_channel'))
        if not ctx.guild.me.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("I am not playing any songs ._.")
        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg("not_in_same_vc"))
        player = music_.get_player(guild_id=ctx.guild.id)
        if not player:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("I am not playing any songs ._.")
        try:
            await player.pause()
        except DiscordUtils.NotPlaying:
            return await ctx.reply("I am not playing any songs ._.")
        await ctx.message.add_reaction("⏸️")

    @commands.command(help="Resume the song.")
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def resume(self, ctx):
        if not ctx.author.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg('not_in_voice_channel'))
        if not ctx.guild.me.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("I am not in a voice channel ._.")
        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg("not_in_same_vc"))
        player = music_.get_player(guild_id=ctx.guild.id)
        if not player:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("I am not playing any songs ._.")
        try:
            await player.resume()
        except DiscordUtils.NotPlaying:
            return await ctx.reply("I am not playing any songs ._.")
        await ctx.message.add_reaction("▶️")

    @commands.command(help="Stop the player.")
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def stop(self, ctx):
        if not ctx.author.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg('not_in_voice_channel'))
        if not ctx.guild.me.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("I am not in a voice channel ._.")
        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg("not_in_same_vc"))
        player = music_.get_player(guild_id=ctx.guild.id)
        if not player:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("I am not playing any songs ._.")
        try:
            await player.stop()
        except DiscordUtils.NotPlaying:
            return await ctx.reply("I am not playing any songs ._.")
        await ctx.message.add_reaction("⏹️")

    @commands.command(help="Toggle song loop!")
    @commands.cooldown(3, 10, commands.BucketType.user)
    async def loop(self, ctx):
        if not ctx.author.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg('not_in_voice_channel'))
        if not ctx.guild.me.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("I am not in a voice channel ._.")
        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg("not_in_same_vc"))
        player = music_.get_player(guild_id=ctx.guild.id)
        if not player:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("There is no music playing, please queue some songs.")
        try:
            song = await player.toggle_song_loop()
        except DiscordUtils.NotPlaying:
            return await ctx.reply("I am not playing any songs ._.")
        if song.is_looping:
            await ctx.reply(f"🔁 Looping `{song.name}`.")
        else:
            await ctx.reply("🔁 Loop disabled.")

    @commands.command(help="Check the song queue!", aliases=['q'])
    async def queue(self, ctx):
        if not ctx.author.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg('not_in_voice_channel'))
        if not ctx.guild.me.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("I am not in a voice channel ._.")
        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg("not_in_same_vc"))
        player = music_.get_player(guild_id=ctx.guild.id)
        if not player:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("There is no music playing, please queue some songs.")
        try:
            queue_ = player.current_queue()
        except DiscordUtils.EmptyQueue:
            return await ctx.reply("The queue is empty ._.")

        nice = ""
        i = 1
        for song_ in queue_:  # i will paginate this later when i feel like not being lazy
            if i == 11:
                break
            nice += f"`{i}.{' ' if i != 10 else ''}` • [{song_.title}]({song_.url})\n"
            i += 1

        return await ctx.reply(embed=success_embed(
            ":notes: Queue!",
            nice
        ))

    @commands.command(help="Skip a song.", aliases=['voteskip'])
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def skip(self, ctx):
        if not ctx.author.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg('not_in_voice_channel'))
        if not ctx.guild.me.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("I am not in a voice channel ._.")
        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg("not_in_same_vc"))
        player = music_.get_player(guild_id=ctx.guild.id)
        if not player:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("There is no music playing, please queue some songs.")
        if not ctx.voice_client.is_playing():
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("There is no music playing ._.")

        hoomans = len(list(filter(lambda m: not m.bot, ctx.author.voice.channel.members)))
        if hoomans <= 2 or ctx.author.guild_permissions.manage_guild:
            try:
                await player.skip(force=True)
                await ctx.message.add_reaction('⏭️')
                if ctx.guild.id in self.skip_votes:
                    self.skip_votes.pop(ctx.guild.id)
                return
            except DiscordUtils.NotPlaying:
                return await ctx.reply("There is no music playing ._.")

        if ctx.guild.id not in self.skip_votes:
            self.skip_votes.update({ctx.guild.id: [ctx.author.id]})
            await ctx.reply(f"⏭️ Vote skipping has been started: `1/{round(hoomans/2)}` votes.")
        else:
            old_list = self.skip_votes[ctx.guild.id]
            if ctx.author.id in old_list:
                return await ctx.reply("You have already added your skip vote!")
            old_list.append(ctx.author.id)
            self.skip_votes.update({ctx.guild.id: old_list})
            if len(self.skip_votes[ctx.guild.id]) >= round(hoomans / 2):
                try:
                    await player.skip(force=True)
                    self.skip_votes.pop(ctx.guild.id)
                    await ctx.message.add_reaction('⏭️')
                except DiscordUtils.NotPlaying:
                    return await ctx.reply("There is no music playing ._.")
            else:
                await ctx.reply(f"⏭️ Skip vote added: `{len(self.skip_votes[ctx.guild.id])}/{round(hoomans/2)}` votes.")

    @commands.command(help="Remove a song from the queue!")
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def remove(self, ctx: commands.Context, index: str = None):
        if not ctx.author.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg('not_in_voice_channel'))
        if not ctx.guild.me.voice:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("I am not in a voice channel ._.")
        if ctx.author.voice.channel != ctx.guild.me.voice.channel:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(self.error_msg("not_in_same_vc"))
        player: MusicPlayer = music_.get_player(guild_id=ctx.guild.id)
        if not player:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("There is no music playing, please queue some songs.")
        if not ctx.voice_client.is_playing():
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("There is no music playing ._.")

        prefix = ctx.clean_prefix
        if index is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(f"{prefix}remove <index>")
        try:
            index = int(index)
            if index <= 0:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(f"{EMOJIS['tick_no']}The number should be a positive number!")
        except ValueError:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(f"Please enter an integer!\n\nUsage: `{prefix}remove <number>`\nExample: `{prefix}remove 69`")
        try:
            song = await player.remove_from_queue(index)
            return await ctx.reply(f"{EMOJIS.get('tick_yes')} Removed `{song.name}` from the queue!")
        except Exception as e:
            return await ctx.reply(f"{e}")

    @commands.command(help="Get lyrics of a song.")
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def lyrics(self, ctx: commands.Context, *, song=None):
        error_msg = f"Please enter the song name.\nExample: `{ctx.clean_prefix}lyrics Never Gonna Give You Up`"
        if song is None:
            player = music_.get_player(guild_id=ctx.guild.id)
            if not player:
                return await ctx.reply(error_msg)
            if not ctx.voice_client.is_playing():
                return await ctx.reply(error_msg)
            current_song = player.now_playing()
            song = current_song.name
        main_msg = await ctx.reply(f"{EMOJIS['loading']} Searching for lyrics...")
        embeds = []
        async with self.client.session.get(f'https://some-random-api.ml/lyrics?title={song.lower()}') as r:
            if r.status != 200:
                return await main_msg.edit("An error occured while accessing the API, please try again later.")
            rj = await r.json()
            if "error" in rj:
                return await ctx.reply(rj['error'])
            if len(rj['lyrics']) <= 4000:
                return await ctx.reply(embed=discord.Embed(
                    title=rj['title'],
                    url=rj['links']['genius'],
                    description=rj['lyrics'],
                    color=MAIN_COLOR
                ).set_thumbnail(url=rj['thumbnail']['genius']))
            i = 0
            while True:
                if len(rj['lyrics']) - i > 4000:
                    embeds.append(discord.Embed(
                        title=rj['title'],
                        url=rj['links']['genius'],
                        description=rj['lyrics'][i:i + 3999],
                        color=MAIN_COLOR
                    ).set_thumbnail(url=rj['thumbnail']['genius']))
                elif len(rj['lyrics']) - i <= 0:
                    break
                else:
                    embeds.append(discord.Embed(
                        title=rj['title'],
                        url=rj['links']['genius'],
                        description=rj['lyrics'][i:len(rj['lyrics']) - 1],
                        color=MAIN_COLOR
                    ).set_thumbnail(url=rj['thumbnail']['genius']))
                    break
                i += 3999
            return await main_msg.edit(content="", embed=embeds[0], view=Paginator(ctx=ctx, embeds=embeds))


def setup(client):
    client.add_cog(music(client))

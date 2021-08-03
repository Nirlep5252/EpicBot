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

from discord.ext import commands
from typing import Union
from utils.embed import error_embed, success_embed
from config import EMOJIS, MAIN_COLOR
from utils.bot import EpicBot
from utils.ui import Confirm


class emojis(commands.Cog, description="Emoji related commands!"):
    def __init__(self, client: EpicBot):
        self.client = client

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.command(help="Enlarge an emoji.")
    async def enlarge(self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji, str] = None):
        prefix = ctx.clean_prefix
        if emoji is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter an emoji to enlarge.\nCorrect Usage: `{prefix}enlarge <emoji>`"
            ))
        if isinstance(emoji, str):
            raise commands.EmojiNotFound(emoji)
        await ctx.reply(emoji.url)

    @commands.command(help="Clone emojis!", aliases=['clone-emoji', 'cloneemoji'])
    @commands.has_permissions(manage_emojis=True)
    @commands.bot_has_permissions(manage_emojis=True)
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def clone(self, ctx, emojis: commands.Greedy[Union[discord.PartialEmoji, discord.Emoji]] = None):
        prefix = ctx.clean_prefix
        if emojis is None:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter some emojis to clone.\n\n**Example:** {prefix}clone {EMOJIS['heawt']} {EMOJIS['shy_uwu']} ..."
            ))
        uploaded_emojis = ""
        failed_emojis = ""

        m = await ctx.reply(f"Cloning please wait... {EMOJIS['loading']}")

        for emoji in emojis:
            if isinstance(emoji, discord.PartialEmoji):
                try:
                    emo = await ctx.guild.create_custom_emoji(
                        name=emoji.name,
                        image=await emoji.read(),
                        reason=f"Clone command used by {ctx.author} ({ctx.author.id})"
                    )
                    uploaded_emojis += f"{emo} "
                except Exception:
                    failed_emojis += f"`{emoji.name}` "
            else:
                view = Confirm(context=ctx)
                await m.edit(
                    content="",
                    embed=success_embed(
                        "Is this the emoji you wanted?",
                        f"The name `{emoji.name}` corresponds to this emote, do u want to clone this?"
                    ).set_image(url=emoji.url),
                    view=view
                )
                await view.wait()
                if view.value is None:
                    await m.edit(
                        content="",
                        embed=error_embed(
                            "You didn't respond in time.",
                            f"Skipped this emoji. Cloning other emojis... {EMOJIS['loading']}"
                        ),
                        view=None
                    )
                elif not view.value:
                    await m.edit(
                        content="",
                        embed=success_embed(
                            f"{EMOJIS['tick_yes']} Alright!",
                            "Skipped that emote."
                        ),
                        view=None
                    )
                else:
                    await m.edit(
                        content="",
                        embed=discord.Embed(
                            title=f"{EMOJIS['tick_yes']} Ok, cloning...",
                            color=MAIN_COLOR
                        ),
                        view=None
                    )
                    try:
                        emo = await ctx.guild.create_custom_emoji(
                            name=emoji.name,
                            image=await emoji.read(),
                            reason=f"Clone command used by {ctx.author} ({ctx.author.id})"
                        )
                        uploaded_emojis += f"{emo} "
                    except Exception:
                        failed_emojis += f"`{emoji.name}` "

        await m.edit(
            content=f"I have cloned {uploaded_emojis}{' and failed to clone '+failed_emojis if len(failed_emojis) > 0 else ''}",
            embed=None,
            view=None
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        guild_config = await self.client.get_guild_config(message.guild.id)
        if not guild_config['nqn']:
            return
        for e in self.client.blacklisted_cache:
            if message.author.id == e['_id']:
                return
        pain = message.content.split(" ")
        final_msg = ""
        for e in pain:
            hmm = e.split(":")
            if len(hmm) < 3:
                final_msg += e + " "
            else:
                i = 1
                interseting = ""
                for h in range(0, len(hmm)):
                    ee = hmm[h]
                    if i % 2 == 0:
                        emoji = discord.utils.get(self.client.emojis, name=ee)
                        if emoji is not None and (hmm[h + 1][18: 19] != ">"):
                            interseting += str(emoji)
                        else:
                            interseting += ":" + ee + (":" if len(hmm) != i else "")
                    else:
                        interseting += ee
                    i += 1
                final_msg += interseting + " "
        if final_msg not in [message.content, message.content[:-1], message.content + " "]:
            msg_attachments = []
            for attachment in message.attachments:
                uwu = await attachment.to_file()
                msg_attachments.append(uwu)
            await message.delete()
            webhooks = await message.channel.webhooks()
            webhook = discord.utils.get(webhooks, name="EpicBot NQN", user=self.client.user)
            if webhook is None:
                webhook = await message.channel.create_webhook(name="EpicBot NQN")

            await webhook.send(
                final_msg,
                files=msg_attachments,
                username=message.author.name,
                avatar_url=message.author.avatar.url,
                allowed_mentions=discord.AllowedMentions.none()
            )


def setup(client):
    client.add_cog(emojis(client))
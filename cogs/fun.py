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
import random
import asyncio
import pyfiglet

from discord.ext import commands
from typing import Optional, Union
from config import (
    EMOJIS, MAIN_COLOR, BIG_PP_GANG, NO_PP_GANG,
    RED_COLOR, ORANGE_COLOR, PINK_COLOR, CHAT_BID,
    CHAT_API_KEY, PINK_COLOR_2
)
from utils.embed import success_embed, error_embed, edit_msg_multiple_times
from utils.custom_checks import voter_only, not_opted_out
from utils.random import email_fun, passwords, DMs, discord_servers
from utils.reddit import pick_random_url_from_reddit
from owotext import OwO
from dadjokes import Dadjoke
from discord.utils import escape_markdown
from utils.bot import EpicBot
from epicbot_images import effects
from io import BytesIO

uwu = OwO()
dadjoke = Dadjoke()


class fun(commands.Cog, description="Wanna have some fun?"):
    def __init__(self, client: EpicBot):
        self.client = client
        self.cb_spam_prevention = commands.CooldownMapping.from_cooldown(1, 20, commands.BucketType.user)
        self.cb_spam_2 = commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.user)
        self.sniped_msgs = {}
        self.edited_msgs = {}
        self.embed_snipes = {}

        self.beer_parties = {}
        self.drank_beer = {}

    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.cooldown(1, 120, commands.BucketType.guild)
    @commands.command(help="Pick a random person from the server members list. :D")
    async def anyone(self, ctx: commands.Context, *, text: str = None):
        nice = list(filter(lambda m: not m.bot, ctx.guild.members))
        cutie = random.choice(nice)
        await ctx.send(
            f"{cutie.mention} {'is the chosen one!' if text is None else text}",
            allowed_mentions=discord.AllowedMentions(
                users=True,
                everyone=False,
                roles=False,
                replied_user=False
            )
        )

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(aliases=['shudi', 'should_i', 'shud_i', 'shoudi'], help="The bot will tell you what should you do!\nMake sure you separate your choices with `or`")
    async def shouldi(self, ctx: commands.Context, *, choices: str = None):
        prefix = ctx.clean_prefix
        if choices is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"""
Please enter some choices.
Example: `{prefix}shouldi Vote EpicBot OR Invite EpicBot`
Another Example: `{prefix}shouldi Study OR Procrastinate`
                """
            ))
        options = choices.lower().split(' or ')
        if len(options) in [0, 1]:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"""
You need to enter 2 or more choices separated with `OR`.
Example: `{prefix}shouldi Vote EpicBot OR Invite EpicBot`
Another Example: `{prefix}shouldi Study OR Procrastinate`
                """
            ))
        if options.count(options[0]) == len(options):
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("Are you dumb? They all are the same options!")
        return await ctx.reply(f"You should: **{random.choice(options)}**")

    @commands.command(help="Start a beer party!", aliases=['beerparty'])
    async def beer(self, ctx: commands.Context):
        if ctx.guild.id in self.beer_parties:
            msg = await ctx.fetch_message(self.beer_parties[ctx.guild.id])
            return await ctx.reply(embed=success_embed(
                "A beer party is already active",
                f"[Click here to go to beer party!]({msg.jump_url})"
            ))
        msg = await ctx.send(f"🍻  A beer party has been started by: {ctx.author.mention}")
        await msg.add_reaction('🍻')

        self.beer_parties.update({ctx.guild.id: msg.id})
        self.drank_beer.update({msg.id: []})

        await asyncio.sleep(30)
        msg = await ctx.channel.fetch_message(msg.id)
        if len(self.drank_beer.get(msg.id)) == 0:
            pain = f"No one drank beer with {ctx.author.mention}.\nNot even they drank beer."
        elif len(self.drank_beer.get(msg.id)) == 1:
            pain = f"No one drank beer with {ctx.author.mention}."
        else:
            pain = f"A total of **{len(self.drank_beer.get(msg.id)) - 1}** people drank beer with {ctx.author.mention}"
        await msg.reply(embed=success_embed(
            "🍻  The beer party ended!",
            pain
        ))
        self.beer_parties.pop(ctx.guild.id)
        self.drank_beer.pop(msg.id)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user):
        if user.bot:
            return
        if reaction.emoji != '🍻':
            return
        if user.guild.id not in self.beer_parties:
            return
        if reaction.message.id != self.beer_parties[user.guild.id]:
            return
        array = self.drank_beer.get(reaction.message.id)
        if user.id in array:
            return
        await reaction.message.channel.send(f"**{escape_markdown(str(user.name))}** drank beer.")
        array.append(user.id)
        self.drank_beer.update({reaction.message.id: array})

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Check your PP size!")
    async def pp(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        msg = await ctx.message.reply(embed=discord.Embed(title=f"Calculating PP size... {EMOJIS['loading']}", color=MAIN_COLOR))
        await asyncio.sleep(0.5)

        uwu = random.randint(1, 10)

        if user.id in BIG_PP_GANG:
            pp = f"8{'='*10}D"
            color = MAIN_COLOR
            footer = "big boi pp"
        elif user.id in NO_PP_GANG or random.randint(0, 5) == 1:
            pp = "You have no PP"
            color = RED_COLOR
            footer = "lol"
        else:
            pp = f"8{'='*uwu}D"
            color = MAIN_COLOR
            footer = "ah yes"

        embed = discord.Embed(
            title="Your PP",
            description=pp,
            color=color
        ).set_author(name=user.name, icon_url=user.avatar.url).set_footer(text=footer)

        await msg.edit(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Free Nitro!!!")
    async def freenitro(self, ctx):
        embed = success_embed("FREE NITRO", "[https://discord.gift/NBnj8bySBWr63Q99](https://discord.gg/Zj7h8Fp)")

        try:
            await ctx.message.delete()
        except Exception:
            pass

        await ctx.send(embed=embed)

    @commands.Cog.listener(name="on_message_delete")
    async def snipe_event_lmao(self, message: discord.Message):
        if message.author.bot:
            return
        user_profile = await self.client.get_user_profile_(message.author.id)
        if not user_profile['snipe']:
            return
        msg_attachments = []
        for attachment in message.attachments:
            uwu = await attachment.to_file()
            msg_attachments.append(uwu)
        thing = {
            "content": message.content,
            "author": message.author,
            "channel": message.channel,
            "time": message.created_at.replace(tzinfo=None),
            "attachments": msg_attachments
        }
        if message.channel.id not in self.sniped_msgs:
            return self.sniped_msgs.update({message.channel.id: [thing]})

        array = self.sniped_msgs[message.channel.id]
        if len(array) >= 5:
            array.pop(0)
        array.append(thing)
        return self.sniped_msgs.update({message.channel.id: array})

    @commands.Cog.listener(name="on_message_edit")
    async def editsnipe_event_lmao(self, before, after):
        if before.author.bot:
            return
        if before.content == after.content and len(before.attachments) == 0:
            return
        user_profile = await self.client.get_user_profile_(before.author.id)
        if not user_profile['snipe']:
            return
        msg_attachments = []
        for attachment in before.attachments:
            uwu = await attachment.to_file()
            msg_attachments.append(uwu)
        thing = {
            "before": before.content,
            "after": after.content,
            "author": before.author,
            "channel": before.channel,
            "time": before.created_at.replace(tzinfo=None),
            "attachments": msg_attachments
        }
        if before.channel.id not in self.edited_msgs:
            return self.edited_msgs.update({before.channel.id: [thing]})

        array = self.edited_msgs[before.channel.id]
        if len(array) >= 5:
            array.pop(0)
        array.append(thing)
        return self.edited_msgs.update({before.channel.id: array})

    @commands.Cog.listener("on_message_edit")
    async def embed_snipe_event(self, before, after):
        if len(before.embeds) == len(after.embeds):
            return
        if not before.author.bot:
            user_profile = await self.client.get_user_profile_(before.author.id)
            if not user_profile['snipe']:
                return
        self.embed_snipes.update({before.channel.id: {
            "before": before.embeds,
            "after": after.embeds
        }})

    @not_opted_out()
    @commands.command(help="Someone deleting the embeds? Snipe them.")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def embedsnipe(self, ctx: commands.Context, channel: discord.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        if channel.id not in self.embed_snipes:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} No deleted embeds found!",
                f"No embeds were removed from {channel.mention}."
            ))
        before = self.embed_snipes[channel.id]['before']
        after = self.embed_snipes[channel.id]['after']
        if len(before) == 0:
            await ctx.send("**Before:** None")
            await ctx.send("**After:**", embed=after[0])
        else:
            await ctx.send("**Before:**", embed=before[0])
            if len(after) == 0:
                await ctx.send("**After:** None")
            else:
                await ctx.send("**After:**", embed=after[0])

    @commands.cooldown(1, 15, commands.BucketType.user)
    @not_opted_out()
    @voter_only()
    @commands.command(aliases=['s'], help="Snipe the last deleted message.")
    async def snipe(self, ctx: commands.Context, amount='1', channel: discord.TextChannel = None):
        prefix = ctx.clean_prefix
        if channel is None:
            channel = ctx.channel
        if amount == 'last' and channel.id in self.sniped_msgs:
            amount = len(self.sniped_msgs[channel.id])
        if amount == 'first':
            amount = 1
        try:
            amount = int(amount)
            if amount <= 0:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Positive values only!",
                    "The amount should be a positive integer."
                ))
            if amount > 5:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Too big!",
                    "You can only snipe upto 5 messages!"
                ))
        except Exception:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Not an integer!",
                f"The amount must be an integer!\nExample: `{prefix}snipe 3`"
            ))
        if channel.id not in self.sniped_msgs:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} No deleted messages!",
                f"No messages were deleted in {channel.mention}"
            ))
        if len(self.sniped_msgs[channel.id]) < amount:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} No deleted message!",
                f"This channel has only **{len(self.sniped_msgs[channel.id])}** deleted messages!"
            ))

        thing = self.sniped_msgs[channel.id][len(self.sniped_msgs[channel.id]) - amount]

        embed = discord.Embed(
            description=thing['content'],
            color=MAIN_COLOR,
            timestamp=thing['time']
        ).set_author(name=thing['author'].name, icon_url=thing['author'].avatar.url)

        await ctx.send(embed=embed, files=thing['attachments'])

    @commands.cooldown(1, 15, commands.BucketType.user)
    @not_opted_out()
    @voter_only()
    @commands.command(aliases=['es'], help="Snipe the last edited message.")
    async def editsnipe(self, ctx: commands.Context, amount=1, channel: discord.TextChannel = None):
        prefix = ctx.clean_prefix
        if channel is None:
            channel = ctx.channel
        if amount == 'last' and channel.id in self.edited_msgs:
            amount = len(self.edited_msgs[channel.id])
        if amount == 'first':
            amount = 1
        try:
            amount = int(amount)
            if amount <= 0:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Positive values only!",
                    "The amount should be a positive integer."
                ))
            if amount > 5:
                return await ctx.reply(embed=error_embed(
                    f"{EMOJIS['tick_no']} Too big!",
                    "You can only snipe upto 5 messages!"
                ))
        except Exception:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Not an integer!",
                f"The amount must be an integer!\nExample: `{prefix}editsnipe 3`"
            ))
        if channel.id not in self.edited_msgs:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} No edited messages!",
                f"No messages were edited in {channel.mention}"
            ))
        if len(self.edited_msgs[channel.id]) < amount:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} No edited message!",
                f"This channel has only **{len(self.edited_msgs[channel.id])}** edited messages!"
            ))

        thing = self.edited_msgs[channel.id][len(self.edited_msgs[channel.id]) - amount]

        embed = discord.Embed(
            color=MAIN_COLOR,
            timestamp=thing['time']
        ).set_author(name=thing['author'].name, icon_url=thing['author'].avatar.url
        ).add_field(name="Before:", value=thing['before'] if len(thing['before']) <= 1024 else thing['before'][0: 1023], inline=False
        ).add_field(name="After:", value=thing['after'] if len(thing['after']) <= 1024 else thing['after'][0: 1023], inline=False)

        await ctx.send(embed=embed, files=thing['attachments'])

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(aliases=['cute'], help="Shows how cute you are, I know you are a cutie!")
    async def howcute(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(
            title="Calculating cuteness...",
            color=MAIN_COLOR
        )
        msg1 = await ctx.message.reply(embed=embed)
        await asyncio.sleep(0.5)

        cute_number = random.randint(0, 100)

        if 0 <= cute_number <= 20:
            lol = "Damn, you're ugly!"
            embed_color_uwu = RED_COLOR
        if 20 < cute_number <= 50:
            lol = "Not bad!"
            embed_color_uwu = ORANGE_COLOR
        if 50 < cute_number <= 75:
            lol = "You're kinda cute, UwU"
            embed_color_uwu = MAIN_COLOR
        if 75 < cute_number <= 100:
            lol = "Holy fuck, you're cute! ><"
            embed_color_uwu = MAIN_COLOR

        embed = discord.Embed(
            title="Cuteness detector!",
            description=f"**{escape_markdown(str(user))}** is **{cute_number}%** cute!",
            color=embed_color_uwu
        )
        embed.set_footer(text=lol)

        await msg1.edit(embed=embed)

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(aliases=['horny'], help="Check how horny someone is 😏")
    async def howhorny(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(
            title="Calculating how horny you are...",
            color=MAIN_COLOR
        )
        msg = await ctx.message.reply(embed=embed)
        await asyncio.sleep(0.5)

        percentage = random.randint(0, 100)

        if 0 <= percentage <= 20:
            lol = "You are a happy person."
            embed_color_uwu = MAIN_COLOR
        if 20 < percentage <= 50:
            lol = "Hmm"
            embed_color_uwu = ORANGE_COLOR
        if 50 < percentage <= 75:
            lol = "You're kinda horny, OwO"
            embed_color_uwu = MAIN_COLOR
        if 75 < percentage <= 100:
            lol = "You are very horny!"
            embed_color_uwu = PINK_COLOR

        await msg.edit(
            embed=discord.Embed(
                title="Hornyness detector!",
                description=f"**{escape_markdown(str(user))}** is **{percentage}%** horny!",
                color=embed_color_uwu
            ).set_footer(text=lol)
        )

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(help="Calculates how gay the user is!", aliases=['gay'])
    async def howgay(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(
            title="Calculating how gay you are...",
            color=MAIN_COLOR
        )
        msg = await ctx.message.reply(embed=embed)
        await asyncio.sleep(0.5)

        cute_number = random.randint(0, 100)

        if 0 <= cute_number <= 20:
            embed_color_uwu = RED_COLOR
        if 20 < cute_number <= 50:
            embed_color_uwu = ORANGE_COLOR
        if 50 < cute_number <= 100:
            embed_color_uwu = MAIN_COLOR

        embed = discord.Embed(
            title="Gayness Detector!",
            description=f"**{escape_markdown(str(user))}** is **{cute_number}%** gay!",
            color=embed_color_uwu
        )

        await msg.edit(embed=embed)

    @commands.command(aliases=['fm', 'firstmsg', 'firstmessage', 'first_msg'], help="Get the first message of the channel.")
    @commands.cooldown(3, 30, commands.BucketType.user)
    @commands.bot_has_permissions(read_message_history=True)
    async def first_message(self, ctx: commands.Context, channel: Optional[discord.TextChannel] = None):
        channel = channel or ctx.channel
        async for message in channel.history(limit=1, oldest_first=True):
            return await ctx.reply(embed=discord.Embed(
                title=f"First message in `{channel.name}`",
                url=message.jump_url,
                color=MAIN_COLOR
            ))

    @commands.Cog.listener("on_message")
    async def chatbot_lmao(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content == "":
            return
        g_conf = await self.client.get_guild_config(message.guild.id)
        if g_conf['chatbot'] != message.channel.id:
            return
        if message.channel.slowmode_delay < 5:
            try:
                await message.channel.edit(slowmode_delay=5)
            except Exception:
                bucket_pain = self.cb_spam_prevention.get_bucket(message)
                retry_after = bucket_pain.update_rate_limit()
                if not retry_after:
                    await message.channel.send("This channel needs to have slowmode of atleast **5 seconds** for chatbot to work!")
                return
        ctx = await self.client.get_context(message)
        await ctx.invoke(self.client.get_command('chat'), message=message.content)

    @commands.cooldown(3, 8, commands.BucketType.user)
    @commands.command(help="Chat with me! >~<")
    async def chat(self, ctx: commands.Context, *, message: str = None):
        BASE_URL = f"http://api.brainshop.ai/get?bid={CHAT_BID}&key={CHAT_API_KEY}"
        async with ctx.channel.typing():
            if message is None:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(
                    f"Hello! In order to chat with me use: `{ctx.clean_prefix}chat <message>`"
                )

            async with self.client.session.get(f"{BASE_URL}&uid={ctx.author.id}&msg={discord.utils.escape_mentions(message)}") as r:
                if r.status != 200:
                    return await ctx.reply("An error occured while accessing the chat API!")
                j = await r.json()
                await ctx.reply(j['cnt'], mention_author=True)

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(help="Check when you are going to die!")
    async def whendie(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author

        msg = await ctx.message.reply(embed=discord.Embed(title="Let's see when you're gonna die...", color=MAIN_COLOR))

        something = [
            f'{random.randint(0, 60)} Second(s)',
            f'{random.randint(1, 60)} Minute(s)',
            f'{random.randint(1, 24)} Hour(s)',
            f'{random.randint(1, 7)} Day(s)',
            f'{random.randint(1, 4)} Week(s)',
            f'{random.randint(1, 100)} Year(s)'
        ]

        thingy = random.choice(something)

        if thingy == something[0]:
            funny_text = "LOL YOU'RE DEAD"
            embed_color = RED_COLOR
        if thingy == something[1]:
            funny_text = "Well rip, you're almost dead"
            embed_color = RED_COLOR
        if thingy == something[2]:
            funny_text = "Sad"
            embed_color = RED_COLOR
        if thingy == something[3]:
            funny_text = "Ok you have some time before you die"
            embed_color = ORANGE_COLOR
        if thingy == something[4]:
            funny_text = "You're not dying that early, Yay!"
            embed_color = ORANGE_COLOR
        if thingy == something[5]:
            funny_text = "Wowie, you have a nice long life! OwO"
            embed_color = MAIN_COLOR

        embed = discord.Embed(
            description=f"**{escape_markdown(str(user))}** is gonna die in **{thingy}**",
            color=embed_color,
        )
        embed.set_author(name=user.name, icon_url=user.avatar.url)
        embed.set_footer(text=funny_text)

        await msg.edit(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['simpfor', 'simp'], help="Simp for someone!")
    async def simp_for(self, ctx: commands.Context, user: discord.Member = None):
        if user is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed("Bruh!", "Please mention someone to simp for"))
        if user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Bruh!",
                "Imagine simping for yourself... why are you so lonely?"
            ))
        if user == self.client.user:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=discord.Embed(
                title=f"{EMOJIS['shy_uwu']} UwU",
                description="Thank you for simping for me!",
                color=PINK_COLOR_2
            ))
        if user.bot:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} You can't simp for bots!",
                "Simp for real people!"
            ))

        user_profile = await self.client.get_user_profile_(user.id)
        user_profile.update({"times_simped": user_profile['times_simped'] + 1})

        embed = discord.Embed(
            title="Wow, what a simp!",
            description=f"""
**{escape_markdown(ctx.author.name)}** is now simping for **{escape_markdown(user.name)}**.
                        """,
            color=PINK_COLOR_2
        ).set_footer(text=f"They now have {user_profile['times_simped']} simp{'s' if user_profile['times_simped'] != 1 else ''}!"
        ).set_thumbnail(url="https://cdn.discordapp.com/emojis/799530519557177374.png")
        await ctx.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Make your text cuter! OwO >~<")
    async def owo(self, ctx, *, message=None):
        if message is None:
            ctx.command.reset_cooldown(ctx)
            message = "Hi! you need to enter a message to owoify it!"
            return await ctx.reply(uwu.whatsthis(message))

        await ctx.send(uwu.whatsthis(message))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Reverse your text.")
    async def reverse(self, ctx, *, message=None):
        example_text = "backwards text go brr"
        prefix = ctx.clean_prefix
        if message is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter a message to reverse.\nCorrect Usage: `{prefix}reverse {example_text}`\nOutput: `{example_text[::-1]}`"
            ))
        await ctx.send(message[::-1])

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Convert your text into a mock")
    async def mock(self, ctx, *, text=None):

        PREFIX = ctx.clean_prefix

        if text is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed("Incorrect Usage!", f"Please enter some text next time!\nCorrect Usage: `{PREFIX}mock <text>`"))

        res = ""
        i = 0
        for c in text:
            if i % 2 == 0:
                res += c.lower()
            else:
                res += c.upper()
            i += 1
        await ctx.reply(res)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=["atc"], help="Makes your text look beautiful")
    async def aesthetic(self, ctx, *, args=None):
        PREFIX = ctx.clean_prefix
        if args is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed("Invalid args", f"Correct usage: `{PREFIX}atc <msg> | [mode]`.\nMode can be `b` (bold), `i` (italic), or `n` (none).\n\nExample: `{PREFIX}atc uwu | n`\nOutput: `u w u`"))

        if args.count(" | ") == 0:
            m = "n"
        else:
            m = args[-1]

        s = ""
        s += "**" if m == "b" else ("_" if m == "i" else "")

        msg = args.split(" | ")[0]
        args = args.split(" | ")[:-1]
        for c in msg:
            s += c + " "
        s += "**" if m == "b" else ("_" if m == "i" else "")

        await ctx.reply(s)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Funny, funny jokes!", aliases=['dadjoke'])
    async def joke(self, ctx):
        await ctx.message.reply(embed=success_embed("Haha!", dadjoke.joke))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Funny, funny memes!")
    async def meme(self, ctx):
        await ctx.message.reply(embed=await pick_random_url_from_reddit('dankmemes', 'Haha!'))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Get a random quote!")
    async def quote(self, ctx):
        async with self.client.session.get('https://type.fit/api/quotes') as r:
            results = await r.json(content_type=None)
        result = random.choice(results)
        await ctx.message.reply(embed=success_embed("Quote!", f"{result['text']} ~ {result['author']}"))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Get a random advice!")
    async def advice(self, ctx):
        async with self.client.session.get('https://api.adviceslip.com/advice') as r:
            result = await r.json(content_type=None)
        await ctx.message.reply(embed=success_embed("Advice!", result['slip']['advice']))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="I will repeat whatever you say!")
    async def say(self, ctx, *, message=None):
        if message is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed("Bruh!", "Please enter something to say next time!"))
        try:
            await ctx.message.delete()
        except Exception:
            pass
        await ctx.send(message)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(help="Convert your text to ascii.")
    async def ascii(self, ctx: commands.Context, *, text: Union[discord.Member, str] = None):
        if text is None and len(ctx.message.attachments) == 0:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(f"{EMOJIS['tick_no']}Please enter some text or upload an image or mention a user.")

        file_bytes = None

        if text is None:
            for attachment in ctx.message.attachments:
                if attachment.content_type == "image/png":
                    file_bytes = await attachment.read()
                    break
            if file_bytes is None:
                ctx.command.reset_cooldown(ctx)
                return await ctx.reply(f"{EMOJIS['tick_no']}Only `png` format is allowed.")

        if isinstance(text, discord.Member):
            file_bytes = await text.avatar.replace(format='png', size=256).read()

        if isinstance(text, str):
            res = pyfiglet.figlet_format(text)
        else:
            res = await effects.ascii(file_bytes)

        try:
            await ctx.reply(f"```{res}```")
        except Exception:
            buffer = BytesIO(res.encode("utf-8"))
            await ctx.reply(file=discord.File(buffer, filename="ascii.txt"))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['answer', '8ball'], help="8ball will answer your question!")
    async def predict(self, ctx, *, question=None):
        if question is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed("Bruh!", "Please enter a question!"))
        responses = ['Yes. <a:EpicTick:760828595823837194>', 'No. <a:EpicCross:760830174207016980>', 'Probably. ', 'Maybe.', 'IDK bro ', 'Seems like it.', 'Nahh.', 'Oh hell yeah.', 'Yes Definitely.', 'I Think not', 'lol no bro', 'Concentrate and ask again', 'Ask a better question lol', 'Umm Yes', 'Umm No', 'Yes lmao', 'No, but imagine if it was yes lol', 'Yes, but imagine if it was no lol', 'hmm, good question', 'Yes, obviously', 'Definitely not']
        await ctx.message.reply(embed=discord.Embed(description="🎱 " + random.choice(responses), color=MAIN_COLOR))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Gives you a random name.")
    async def randomname(self, ctx):
        async with self.client.session.get('https://nekos.life/api/v2/name') as r:
            result = await r.json()
        await ctx.message.reply(embed=success_embed("Random Name!", result['name']))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Flip a coin!", aliases=['coin'])
    async def coinflip(self, ctx):
        outcomes = ['Heads', 'Tails']

        embed = discord.Embed(
            title="Flipping the Coin... :coin:",
            color=MAIN_COLOR
        )
        msg = await ctx.message.reply(embed=embed)
        await asyncio.sleep(0.5)
        await msg.edit(embed=success_embed("Coin!", f"Result: **{random.choice(outcomes)}**"))

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Roll a dice!")
    async def dice(self, ctx):
        embed = discord.Embed(
            title="Rolling Dice...",
            color=MAIN_COLOR
        )
        msg = await ctx.message.reply(embed=embed)
        await asyncio.sleep(0.5)
        await msg.edit(embed=success_embed("Dice!", f"You rolled a **{random.randint(1, 6)}**"))

    @commands.cooldown(1, 45, commands.BucketType.user)
    @commands.command(help="Hack someone!", category="economy")
    async def hack(self, ctx: commands.Context, user: discord.Member = None):
        if user is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed("Bruh!", "Please mention who do you want to hack next time!"))

        if user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed("Bruh!", "Don't hack yourself idiot!"))
        if user.bot:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=error_embed("Bruh!", "You can't hack bots.\nThey are way too powerful!"))

        email_username = ""
        for e in user.name:
            if e == " ":
                e = "_"
            email_username += e.lower()
        email_address = f"{email_username}{random.choice(email_fun).lower()}@gmail.com"
        password = random.choice(passwords)
        latest_dm = random.choice(DMs)
        most_used_discord_server = random.choice(discord_servers)

        uwu_lmao = discord.Embed(
            title=f"{escape_markdown(str(user.name))}'s Data {EMOJIS['hacker_pepe']}",
            description=f"""
**Email:** `{email_address}`
**Password:** `{password}`
**Most Used Discord Server:** `{most_used_discord_server}`
**Latest DM:** `{latest_dm}`
            """,
            color=MAIN_COLOR
        )

        await edit_msg_multiple_times(
            ctx, 1, f"Initializing `hack.exe` {EMOJIS['hacker_pepe']}",
            [
                [f"Successfully initialized `hack.exe`, beginning hacks... {EMOJIS['loading']}"],
                [f"Logging into {user.name}'s Discord Account... {EMOJIS['loading']}"],
                [f"Successfully Logged in! {EMOJIS['tick_yes']}", f"**Email Address:** `{email_address}`\n**Password:** `{password}`"],
                [f"Fetching DMs from friends (if there are any)... {EMOJIS['loading']}"],
                [f"Latest DM from {user.name}", latest_dm],
                [f"Fetching the most used Discord server... {EMOJIS['loading']}"],
                [f"Most used Discord server found {EMOJIS['tick_yes']}", most_used_discord_server],
                [f"Selling data... {EMOJIS['loading']}"]
            ],
            uwu_lmao
        )


def setup(client):
    client.add_cog(fun(client))

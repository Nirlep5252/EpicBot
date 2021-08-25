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
import datetime
import time
import asyncio
import aiohttp
import json
import re

from config import EMOJIS, MAIN_COLOR, UD_API_KEY, RED_COLOR, WEATHER_API_KEY
from utils.embed import success_embed, error_embed, process_embeds_from_json
from utils.time import convert
from utils.random import gen_random_string
from discord.ext import commands, tasks
from discord.utils import escape_markdown
from utils.ui import Confirm, Paginator
from utils.bot import EpicBot
from utils.message import wait_for_msg

afk_users = []
afk_reasons = {}
afk_guilds = {}


class utility(commands.Cog, description="Commands that make your Discord experience nicer!"):
    def __init__(self, client: EpicBot):
        self.client = client
        self.reminding.start()
        self.regex = re.compile(r"(\w*)\s*(?:```)(\w*)?([\s\S]*)(?:```$)")

    @property
    def session(self):
        return self.client.http._HTTPClient__session  # type: ignore

    async def _run_code(self, *, lang: str, code: str):
        res = await self.session.post(
            "https://emkc.org/api/v1/piston/execute",
            json={"language": lang, "source": code},
        )
        return await res.json()

    @tasks.loop(seconds=1)
    async def reminding(self):
        for e in self.client.reminders:
            if round(e['time']) <= round(time.time()):
                user = self.client.get_user(e['user_id'])
                embed = success_embed(
                    f"{EMOJIS['reminder']} Reminder!",
                    f"{e['reminder']}\n\nYou set this reminder <t:{round(e['set_time'])}:R>"
                )
                try:
                    await user.send(embed=embed)
                except Exception as e_:
                    print(e_)
                index = self.client.reminders.index(e)
                self.client.reminders.pop(index)
                await self.client.reminders_db.delete_one({"_id": e['_id'], "user_id": e['user_id']})

    @commands.cooldown(2, 30, commands.BucketType.user)
    @commands.command(help="I will remind you whatever you tell me to.", aliases=['remind', 'remind_me', 'reminder'])
    async def remindme(self, ctx: commands.Context, time__=None, *, reminder: str = None):
        prefix = ctx.clean_prefix
        example = f"`{prefix}remindme 10h message egirl`"
        usage = f"`{prefix}remindme <time> <reminder>`"
        if time__ is None or reminder is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter a time and reminder.\nCorrect Usage: {usage}\nExample: {example}"
            ))
        time_ = convert(time__)
        if time_ == -1:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Unit of time.",
                f"Please enter a valid unit of time.\nValid units are: `s, m, h, d, w, y`\nExample: {example}"
            ))
        if time_ == -2:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Args!",
                f"The time argument should be an integer followed by a unit.\nExample: {example}"
            ))
        if time_ == -3:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Positive values only!",
                "The value of time should be positive values only."
            ))
        reminder_limit = 250
        if len(reminder) >= reminder_limit:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Too long!",
                f"The reminder can't be longer than **{reminder_limit}** characters."
            ))
        time_in_seconds = time_[0]
        if time_in_seconds > 43200 * 60 * 12:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Too long!",
                "Reminders can't be longer than **1 year**."
            ))

        random_id = gen_random_string(10)

        aaaaaa_pain = {
            "_id": random_id,
            "user_id": ctx.author.id,
            "set_time": time.time(),
            "time": (time.time() + time_in_seconds),
            "reminder": reminder
        }

        await ctx.reply(embed=success_embed(
            f"{EMOJIS['tick_yes']} Alright!",
            f"I will remind you <t:{round(time.time() + time_in_seconds)}:R> on <t:{round(time.time() + time_in_seconds)}:F>."
        ).set_footer(text=f"You can use {prefix}reminders to check your remiders."))

        self.client.reminders.append(aaaaaa_pain)
        await self.client.reminders_db.insert_one(aaaaaa_pain)

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command(help="Delete your reminder.", aliases=['delete_reminder', 'delremind', 'del_reminder', 'del_remind'])
    async def delreminder(self, ctx, id_=None):
        prefix = ctx.clean_prefix
        if id_ is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter an id.\nCorrect Usage: `{prefix}delreminder <id>`\nExample: `{prefix}delreminder s0MUcHp41N`"
            ))
        for e in self.client.reminders:
            if e["_id"] == id_ and e["user_id"] == ctx.author.id:
                await ctx.reply(embed=success_embed(
                    f"{EMOJIS['tick_yes']} Deleted!",
                    f"The reminder with ID: `{id_}` has been deleted."
                ).add_field(name="More Info:", value=f"```yaml\nReminder: {e['reminder']}\nTime: {time.ctime(e['time'])}\n```"))
                self.client.reminders.pop(self.client.reminders.index(e))
                await self.client.reminders_db.delete_one({"_id": id_, "user_id": ctx.author.id})
                return
        return await ctx.reply(embed=error_embed(
            f"{EMOJIS['tick_no']} Not found!",
            f"The reminder with ID: `{id_}` does not exist."
        ))

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(help="Check your current reminders!")
    async def reminders(self, ctx):
        prefix = ctx.clean_prefix
        embed = discord.Embed(
            title=f"{EMOJIS['reminder']} Your Reminders!",
            color=MAIN_COLOR
        )
        ah_yes = self.client.reminders
        pain = []
        for e in ah_yes:
            if e['user_id'] == ctx.author.id:
                pain.append(e)
        if len(pain) == 0:
            embed.description = f"You don't have any reminders set.\nYou can use `{prefix}remindme <time> <reminder>` to set a reminder."
        else:
            for aa in pain:
                embed.add_field(
                    name=f"ID: `{aa['_id']}`",
                    value=f"{aa['reminder']} - <t:{round(aa['time'])}:F> <t:{round(aa['time'])}:R>",
                    inline=False
                )
            embed.set_footer(text=f"You can delete reminders using {prefix}delreminder <id>")
        await ctx.reply(embed=embed)

    @commands.command(help="Run code and get results instantly! Credits: `FalseDev`")
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def run(self, ctx: commands.Context, *, codeblock: str = None):
        if not codeblock:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter a code block.\nCorrect Usage: `{ctx.clean_prefix}run <code>`"
            ))
        matches = self.regex.findall(codeblock)
        if not matches:
            return await ctx.reply(
                embed=error_embed(
                    "Uh-oh", "Please use codeblocks to run your code!"
                ).set_image(url="https://us2.tixte.net/uploads/awish-go.to-sleep.xyz/ksh6nas2u9a.png")
            )
        lang = matches[0][0] or matches[0][1]
        if not lang:
            return await ctx.reply(
                embed=error_embed("Uh-oh", "Couldn't find the language hinted in the codeblock or before it")
            )
        code = matches[0][2]
        result = await self._run_code(lang=lang, code=code)

        await self._send_result(ctx, result)

    async def _send_result(self, ctx: commands.Context, result: dict):
        if "message" in result:
            return await ctx.reply(
                embed=error_embed("Uh-oh", result["message"])
            )
        output = result["output"]
        #        if len(output) > 2000:
        #            url = await create_guest_paste_bin(self.session, output)
        #            return await ctx.reply("Your output was too long, so here's the pastebin link " + url)
        embed = discord.Embed(title=f"Ran your {result['language']} code", color=MAIN_COLOR)
        output = output[:500].strip()
        shortened = len(output) > 500
        lines = output.splitlines()
        shortened = shortened or (len(lines) > 15)
        output = "\n".join(lines[:15])
        output += shortened * "\n\n**Output shortened**"
        embed.add_field(name="Output", value=f"```{output}```" or "**<No output>**")

        await ctx.reply(embed=embed)

    # @commands.cooldown(1, 10, commands.BucketType.user)
    # @commands.command(help="Set an alarm!", aliases=['setalarm'])
    # async def alarm(self, ctx: commands.Context, time_: int = None, timezone: TimeZone = None, *, text: str = None):
    #     pass

    # @commands.cooldown(1, 10, commands.BucketType.user)
    # @commands.command(help="Delete an alarm!")
    # async def delalarm(self, ctx: commands.Context, id_: str):
    #     prefix = ctx.clean_prefix
    #     if id_ is None:
    #         ctx.command.reset_cooldown(ctx)
    #         return await ctx.reply(embed=error_embed(
    #             f"{EMOJIS['tick_no']} Invalid Usage!",
    #             f"Please enter an id.\nCorrect Usage: `{prefix}delalarm <id>`\nExample: `{prefix}delalarm s0MUcHp41N`"
    #         ))
    #     for e in self.client.alarms:
    #         if e["_id"] == id_ and e['user_id'] == ctx.author.id:
    #             await ctx.reply(embed=success_embed(
    #                 f"{EMOJIS['tick_yes']} Deleted!",
    #                 f"The alarm with ID: `{id_}` has been deleted."
    #             ))
    #             self.client.alarms.pop(self.client.alarms.index(e))
    #             await self.client.alarms_db.delete_one({"_id": id_, "user_id": ctx.author.id})
    #             return
    #     return await ctx.reply(embed=error_embed(
    #         f"{EMOJIS['tick_no']} Not found!",
    #         f"The alarm with ID: `{id_}` does not exist."
    #     ))

    # @commands.cooldown(1, 10, commands.BucketType.user)
    # @commands.command(help="Check your current alarms!")
    # async def alarms(self, ctx: commands.Context):
    #     prefix = ctx.clean_prefix
    #     embed = discord.Embed(
    #         title=f"{EMOJIS['reminder']} Your Alarms!",
    #         color=MAIN_COLOR
    #     )
    #     ah_yes = self.client.alarms
    #     pain = []
    #     for e in ah_yes:
    #         if e['user_id'] == ctx.author.id:
    #             pain.append(e)
    #     if len(pain) == 0:
    #         embed.description = f"You don't have any alarms set.\nYou can use `{prefix}alarm <time> <text>` to set an alarm."
    #     else:
    #         for aa in pain:
    #             embed.add_field(
    #                 name=f"ID: `{aa['_id']}`",
    #                 value=f"{aa['text']} - <t:{aa['time']}:t>",
    #                 inline=False
    #             )
    #         embed.set_footer(text=f"You can delete alarms using {prefix}delalarm <id>")
    #     await ctx.reply(embed=embed)

    # @commands.command(help="Start a poll!", aliases=['startpoll', 'createpoll', 'makepoll'])
    # @commands.cooldown(3, 60, commands.BucketType.guild)
    # async def poll(self, ctx: commands.Context, *, question: str):
    #     pass

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(help="Get info about stickers in a message!", aliases=['stickers', 'stickerinfo'])
    async def sticker(self, ctx: commands.Context):
        ref = ctx.message.reference
        if not ref:
            stickers = ctx.message.stickers
        else:
            msg = await ctx.fetch_message(ref.message_id)
            stickers = msg.stickers
        if len(stickers) == 0:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} No Stickers!",
                "There are no stickers in this message."
            ))
        embeds = []
        for sticker in stickers:
            sticker = await sticker.fetch()
            embed = discord.Embed(
                title=f"{EMOJIS['tick_yes']} Sticker Info",
                description=f"""
**Name:** {sticker.name}
**ID:** {sticker.id}
**Description:** {sticker.description}
**URL:** [Link]({sticker.url})
{"**Related Emoji:** "+":"+sticker.emoji+":" if isinstance(sticker, discord.GuildSticker) else "**Tags:** "+', '.join(sticker.tags)}
                """,
                color=MAIN_COLOR
            ).set_thumbnail(url=sticker.url)
            if isinstance(sticker, discord.GuildSticker):
                embed.add_field(
                    name="Guild ID:",
                    value=f"{sticker.guild_id}",
                    inline=False
                )
            else:
                pack = await sticker.pack()
                embed.add_field(
                    name="Pack Info:",
                    value=f"""
**Name:** {pack.name}
**ID:** {pack.id}
**Stickers:** {len(pack.stickers)}
**Description:** {pack.description}
                    """,
                    inline=False
                )
                embed.set_image(url=pack.banner.url)
            embeds.append(embed)

        if len(embeds) == 1:
            await ctx.reply(embed=embeds[0])
        else:
            view = Paginator(ctx, embeds)
            await ctx.reply(embed=embeds[0], view=view)

    @commands.cooldown(3, 30, commands.BucketType.user)
    @commands.command(help="Bookmark a message!", aliases=['bukmark'])
    async def bookmark(self, ctx):
        ref = ctx.message.reference
        if not ref:
            return await ctx.reply("You need to reply to a message in order to bookmark it.")

        bookmarks = await self.client.bookmarks.find_one({"_id": ctx.author.id})
        if bookmarks is not None and len(bookmarks['bookmarks']) >= 25:
            return await ctx.reply("You cannot bookmarks more than `25` messages.")
        msg = await ctx.fetch_message(ref.message_id)
        em = discord.Embed(
            title="Bookmark added!",
            url=msg.jump_url,
            color=MAIN_COLOR,
            description=msg.content,
            timestamp=datetime.datetime.utcnow()
        ).set_author(name=msg.author, icon_url=msg.author.display_avatar.url
        ).set_footer(text=f"Msg ID: {msg.id} | Author ID: {msg.author.id}")
        nice = ""
        for e in msg.attachments:
            nice += f"[{e.filename}]({e.url})\n"
        if len(nice) > 0:
            em.add_field(name="Attachments", value=nice, inline=False)

        try:
            await ctx.author.send(embed=em)
            if msg.author.bot:
                for embed_ in msg.embeds:
                    await ctx.author.send(embed=embed_)
        except Exception:
            return await ctx.reply("Your DMs are closed :<")

        if bookmarks is None:
            await self.client.bookmarks.insert_one({
                "_id": ctx.author.id,
                "bookmarks": [{"url": msg.jump_url, "time": round(time.time()), "id": gen_random_string(10)}]
            })
        else:
            old_list = bookmarks['bookmarks']
            old_list.append({
                "url": msg.jump_url,
                "time": round(time.time()),
                "id": gen_random_string(10)
            })
            await self.client.bookmarks.update_one(
                filter={"_id": ctx.author.id},
                update={"$set": {
                    "bookmarks": old_list
                }},
                upsert=True
            )
        await ctx.message.add_reaction('🔖')

    @commands.command(help="Check your bookmarks.")
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def bookmarks(self, ctx):
        prefix = ctx.clean_prefix
        b = await self.client.bookmarks.find_one({"_id": ctx.author.id})
        if b is None or len(b['bookmarks']) == 0:
            return await ctx.reply("You have `0` bookmarks.")

        bookmarks = ""

        for b_ in b['bookmarks']:
            bookmarks += f"[`{b_['id']}`]({b_['url']}) • <t:{b_['time']}:R>\n"

        await ctx.reply(embed=success_embed(
            "🔖  Your bookmarks",
            f"You have `{len(b['bookmarks'])}` bookmarks.\n\n{bookmarks}"
        ).set_footer(text=f"You can use `{prefix}delbookmark <id>` to delete a bookmark."))

    @commands.command(help="Delete a bookmark.")
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def delbookmark(self, ctx: commands.Context, _id=None):
        if _id is None:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Correct Usage: `{ctx.clean_prefix}delbookmark <id>`\nUse `{ctx.clean_prefix}delbookmark all` to delete all bookmarks."
            ))
        b = await self.client.bookmarks.find_one({"_id": ctx.author.id})
        if b is None:
            return await ctx.reply("You don't any bookmarks ._.")
        if _id.lower() == 'all':
            v = Confirm(context=ctx)
            m = await ctx.reply("Are you sure?", view=v)
            await v.wait()
            if v.value is None:
                return await m.edit(content="You didn't respond in time!", view=None)
            if not v.value:
                return await m.edit(content="Cancelled.", view=None)
            await self.client.bookmarks.update_one(
                filter={"_id": ctx.author.id},
                update={"$set": {
                    "bookmarks": []
                }},
                upsert=True
            )
            return await m.edit(content="All your bookmarks have been reset.", view=None)
        for b_ in b['bookmarks']:
            if b_['id'] == _id:
                b['bookmarks'].remove(b_)
                await self.client.bookmarks.update_one(
                    filter={"_id": ctx.author.id},
                    update={"$set": {
                        "bookmarks": b['bookmarks']
                    }},
                    upsert=True
                )
                return await ctx.reply(f"The bookmark `{_id}` has been deleted.")
        return await ctx.reply(f"Invalid bookmark ID. Please use `{ctx.clean_prefix}bookmarks` to see all your bookmarks.")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Sets you as AFK.")
    async def afk(self, ctx, *, reason=None):
        if ctx.author.id in afk_users:
            return

        await ctx.reply(
            embed=success_embed(
                f"{EMOJIS['sleepy']}  AFK",
                f"I set you as AFK for reason: {reason}"
            )
        )

        old_nick = ctx.author.name if ctx.author.nick is None else ctx.author.nick
        try:
            if not ctx.author.display_name.startswith("[AFK] "):
                await ctx.author.edit(nick=f"[AFK] {old_nick}")
        except Exception:
            pass

        await asyncio.sleep(15)
        afk_users.append(ctx.author.id)
        afk_reasons.update({ctx.author.id: reason})
        afk_guilds.update({ctx.author.id: ctx.guild.id})

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.author.id in afk_users:
            afk_users.remove(message.author.id)
            if message.author.id in afk_guilds:
                guild = self.client.get_guild(int(afk_guilds[message.author.id]))
                afk_guilds.pop(message.author.id)
                if guild:
                    member = guild.get_member(message.author.id)
                    if member:
                        user_nick = member.nick
                        if user_nick is not None and user_nick.startswith("[AFK] "):
                            try:
                                await member.edit(nick=user_nick[6:])
                            except Exception:
                                pass
            return await message.reply(
                embed=success_embed(
                    "Welcome Back!",
                    "I removed you from AFK."
                ),
                delete_after=5
            )
        for user in message.mentions:
            if user.id in afk_users:
                return await message.reply(
                    f"**{escape_markdown(user.name)}** is AFK for: {afk_reasons[user.id]}",
                    delete_after=5
                )

    @commands.cooldown(3, 30, commands.BucketType.user)
    @commands.command(help="Make a completely customizable embed.")
    async def embed(self, ctx: commands.Context):
        m = await ctx.reply(embed=success_embed(
            f"{EMOJIS['loading']} Embed builder...",
            "Please visit the [**Embed Builder**](https://embedbuilder.nadekobot.me/) and generate your embed.\nThen paste the generated code here."
        ).set_footer(text="Make sure you reply within 10 mins."))

        uwu = await wait_for_msg(ctx, 600, m)
        if uwu == 'pain':
            ctx.command.reset_cooldown(ctx)
            return

        try:
            amogus = json.loads(uwu.content)
        except Exception:
            ctx.command.reset_cooldown(ctx)
            return await m.edit(
                f"{EMOJIS['tick_no']}Looks like your embed json code is invalid.\nPlease re-run the command and try again.",
                embed=None
            )

        stuff = await process_embeds_from_json(ctx.bot, [ctx.author, ctx.guild], amogus, replace=False)
        if isinstance(stuff, str):
            ctx.command.reset_cooldown(ctx)
            return await m.edit(
                f"{EMOJIS['tick_no']}Looks like your json embed code had some errors.\nHere's a very helpful error message by Nirlep: `{stuff}`",
                embed=None
            )
        else:
            try:
                await m.delete()
            except Exception:
                pass
            return await ctx.send(content=stuff[0] if stuff[0] is not None else "", embed=stuff[1])

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.command(aliases=['df', 'def', 'urban', 'ud', 'urbandictionary'], help="Check the meaning of a word.")
    async def define(self, ctx: commands.Context, *, ud_query=None):
        prefix = ctx.clean_prefix
        if ud_query is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                "Incorrect Usage!",
                f"Please use the command like this: `{prefix}define <query>`"
            ))
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        querystring = {"term": ud_query}
        headers = {
            "x-rapidapi-key": UD_API_KEY,
            "x-rapidapi-host": "mashape-community-urban-dictionary.p.rapidapi.com",
        }
        async with self.client.session.get(url, headers=headers, params=querystring) as r:
            ud_json = await r.json()
        total_definitions = len(ud_json["list"])
        try:
            word_name = ud_json["list"][1]["word"]
            definition = ud_json["list"][1]["definition"]
            link = ud_json["list"][1]["permalink"]
            example = ud_json["list"][1]["example"]
            more_res = total_definitions - 1

            definition2 = ud_json["list"][0]["definition"]
            example2 = ud_json["list"][0]["example"]

            em_ud = discord.Embed(
                title=str(word_name),
                url=link,
                color=MAIN_COLOR
            )
            em_ud.add_field(name="Definition:", value=definition, inline=False)
            em_ud.add_field(name="Example:", value=example, inline=False)
            em_ud.add_field(name="Definition (2):", value=definition2, inline=False)
            em_ud.add_field(name="Example (2):", value=example2, inline=False)

            em_ud.set_footer(text=f'{more_res} more results.')
            em_ud.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=em_ud)

        except Exception:
            try:
                word_name = ud_json["list"][0]["word"]
                definition = ud_json["list"][0]["definition"]
                link = ud_json["list"][0]["permalink"]
                example = ud_json["list"][0]["example"]
                more_res = total_definitions - 1
                em_ud = discord.Embed(
                    title=str(word_name),
                    url=link,
                    color=MAIN_COLOR
                )
                em_ud.add_field(name="Definition: ", value=definition, inline=False)
                em_ud.add_field(name="Example: ", value=example, inline=False)
                em_ud.set_footer(text=f'{more_res} more results.')
                em_ud.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=em_ud)
            except Exception:
                ctx.command.reset_cooldown(ctx)
                em_ud_no = discord.Embed(
                    title="\"" + str(ud_query) + "\" did not match to any pages. Try another query!",
                    color=RED_COLOR
                )
                em_ud_no.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=em_ud_no)

    @commands.cooldown(2, 10, commands.BucketType.user)
    @commands.command(help="Check the weather!")
    async def weather(self, ctx: commands.Context, *, location=None):
        prefix = ctx.clean_prefix
        if location is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Usage!",
                f"Please enter a location!\nExample: `{prefix}weather london`"
            ))
        location = location.lower()
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
            async with aiohttp.ClientSession() as s:
                async with s.get(url) as r:
                    data = await r.json()
            embed = discord.Embed(
                title=f"Weather for {location.title()}",
                color=MAIN_COLOR
            )
            embed.add_field(
                name="Coordinates:",
                value=f"""
```yaml
Longitude: {data['coord']['lon']}
Latitude: {data['coord']['lat']}
```
                """,
                inline=False
            )
            embed.add_field(
                name="Weather:",
                value=f"""
```yaml
Type: {data['weather'][0]['main'].title()}
Description: {data['weather'][0]['description'].title()}
```
                """,
                inline=False
            )
            embed.add_field(
                name="Temperature:",
                value=f"""
```yaml
Temperature: {data['main']['temp']} °C
Minimum: {data['main']['temp_min']} °C
Maximum: {data['main']['temp_max']} °C
Feels Like: {data['main']['feels_like']} °C
```
                """,
                inline=False
            )
            await ctx.reply(embed=embed)
        except Exception:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                "Error!",
                f"I wasn't find the weather of `{location.title()}`."
            ))


def setup(client):
    client.add_cog(utility(client))

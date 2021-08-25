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

from config import DEFAULT_LEVEL_UP_MSG
from discord import (
    Message,
    Member,
    AllowedMentions,
    Embed,
    File
)
from discord.ext import commands
from utils.embed import success_embed, error_embed
from discord.utils import escape_markdown
from config import MAIN_COLOR, EMOJIS
from operator import itemgetter
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from utils.bot import EpicBot


async def process_level_up_messages(lvl_up_msg, member: Member, level, msg_count):
    nice = {
        "{user_name}": member.name,
        "{user_nickname}": member.display_name,
        "{user_discrim}": str(member.discriminator),
        "{user_tag}": member.name + '#' + str(member.discriminator),
        "{user_mention}": member.mention,
        "{user_id}": member.id,

        "{level}": level,
        "{messages}": msg_count,
    }

    for i, j in nice.items():
        lvl_up_msg = lvl_up_msg.replace(i, str(j))
    return lvl_up_msg


async def get_level(xp):
    lvl = 0
    while True:
        if xp < ((50 * (lvl ** 2)) + 50 * lvl):
            break
        lvl += 1
    return lvl

rank_card_templates = {
    "default": {
        "owner": 529995365714231327,
        "description": "The default rank card!",

        "avatar_resize": 162,
        "avatar_xy": (30, 30),

        "progress_bar_width": 485,
        "progress_bar_height": 18,
        "progress_bar_start_x": 210,
        "progress_bar_start_y": 146,
        "progress_bar_color": (169, 197, 255),

        "username_x": 225,
        "username_y": 90,
        "username_font": ImageFont.truetype("assets/fonts/arial-rounded-mt-bold.ttf", size=30),

        "rank_xy": (540, 25),
        "level_xy": (680, 25),
        "xp_xy": (550, 100),
        "no_xp_text": False,

        "rank_and_level_font": ImageFont.truetype("assets/fonts/berlin-sans.ttf", size=30),
        "xp_font": ImageFont.truetype("assets/fonts/berlin-sans.ttf", size=24)
    },
    "awish": {
        "owner": 671355502399193128,
        "description": "Rank card made by Aw||oo||sh.",

        "avatar_resize": 110,
        "avatar_xy": (222, 35),

        "progress_bar_width": 480,
        "progress_bar_height": 5,
        "progress_bar_start_x": 170,
        "progress_bar_start_y": 165,
        "progress_bar_color": (55, 152, 255),

        "username_x": 350,
        "username_y": 50,
        "username_font": ImageFont.truetype("assets/fonts/red-hat-display-bold.ttf", size=30),

        "rank_xy": (105, 112),
        "level_xy": (105, 25),
        "xp_xy": (425, 104),
        "no_xp_text": True,

        "rank_and_level_font": ImageFont.truetype("assets/fonts/red-hat-display-bold.ttf", size=30),
        "xp_font": ImageFont.truetype("assets/fonts/red-hat-display-bold.ttf", size=27)
    },
    "arto": {
        "owner": 729765852030828674,
        "description": "A Rank card by Arto",

        "avatar_resize": 94,
        "avatar_xy": (31, 51),

        "progress_bar_width": 195,
        "progress_bar_height": 28,
        "progress_bar_start_x": 132,
        "progress_bar_start_y": 147,
        "progress_bar_color": (0, 0, 0),

        "username_x": 255,
        "username_y": 35,
        "username_font": ImageFont.truetype("assets/fonts/gotham_bold.ttf", size=17),
        "username_color": (78, 79, 81),

        "level_xy": (305, 122),
        "level_color": (78, 79, 81),
        "xp_xy": (440, 160),
        "xp_color": (0, 0, 0),
        "no_xp_text": True,

        "rank_and_level_font": ImageFont.truetype("assets/fonts/gotham_bold.ttf", size=17),
        "xp_font": ImageFont.truetype("assets/fonts/gotham_bold.ttf", size=17)
    },
    "yummy": {
        "owner": 529995365714231327,
        "description": "something yummy i did <:poglep_triggered:845559288503992330>",

        "avatar_resize": 164,
        "avatar_xy": (39, 29),

        "progress_bar_width": 489,
        "progress_bar_height": 21,
        "progress_bar_start_x": 217,
        "progress_bar_start_y": 145,
        "progress_bar_color": (255, 255, 255),

        "username_x": 325,
        "username_y": 25,
        "username_font": ImageFont.truetype("assets/fonts/eras-bold-itc.ttf", size=40),

        "rank_xy": (370, 100),
        "level_xy": (660, 100),
        "xp_xy": (550, 180),
        "no_xp_text": False,

        "rank_and_level_font": ImageFont.truetype("assets/fonts/berlin-sans.ttf", size=30),
        "xp_font": ImageFont.truetype("assets/fonts/berlin-sans.ttf", size=20)
    },
    "alien": {
        "owner": 739440618107043901,
        "description": "alien look rankcard by SylmFox",

        "avatar_resize": 325,
        "avatar_xy": (1500, 80),

        "progress_bar_width": 1355 - 9 - 786,
        "progress_bar_height": 436 - 9 - 325,
        "progress_bar_start_x": 786,
        "progress_bar_start_y": 325,
        "progress_bar_color": (30, 213, 195),

        "username_x": 380,
        "username_y": 100,
        "username_font": ImageFont.truetype("assets/fonts/Roboto-Bold.ttf", size=70),

        "rank_xy": (1160, 75),
        "level_xy": (1160, 195),
        "xp_xy": (325, 350),
        "no_xp_text": False,

        "rank_and_level_font": ImageFont.truetype("assets/fonts/Roboto-Bold.ttf", size=50),
        "xp_font": ImageFont.truetype("assets/fonts/Roboto-Bold.ttf", size=55)
    },
    "brixk": {
        "owner": 595490455844683778,
        "description": "Red rankcard using EpicBot logo colour palette",

        "avatar_resize": 442,
        "avatar_xy": (158, 140),

        "progress_bar_width": 1359 - 5 - (737 + 5),
        "progress_bar_height": 575 - 5 - (484 + 5),
        "progress_bar_start_x": 737 + 5,
        "progress_bar_start_y": 484 + 5,
        "progress_bar_color": (145, 28, 37),

        "username_x": 800,
        "username_y": 400,
        "username_font": ImageFont.truetype("assets/fonts/Roboto-Bold.ttf", size=65),

        "rank_xy": (1050, 240),
        "level_xy": (1050, 120),
        "xp_xy": (1020, 590),
        "xp_color": (255, 255, 255),
        "no_xp_text": True,

        "rank_and_level_font": ImageFont.truetype("assets/fonts/Roboto-Bold.ttf", size=50),
        "xp_font": ImageFont.truetype("assets/fonts/Roboto-Bold.ttf", size=30)
    },
    "bloo": {
        "owner": 729765852030828674,
        "description": "A blue colored rank-card",

        "avatar_resize": 189 - 58,
        "avatar_xy": (467, 58),

        "progress_bar_width": 897 - 689 - 10,
        "progress_bar_height": 181 - 156 - 10,
        "progress_bar_start_x": 689 + 5,
        "progress_bar_start_y": 156 + 5,
        "progress_bar_color": (255, 255, 255),

        "username_x": 120,
        "username_y": 130,
        "username_font": ImageFont.truetype("assets/fonts/Roboto-Bold.ttf", size=45),

        "rank_xy": (780, 87),
        "level_xy": (780, 50),
        "xp_xy": (725, 125),
        "no_xp_text": False,

        "rank_and_level_font": ImageFont.truetype("assets/fonts/Roboto-Bold.ttf", size=25),
        "xp_font": ImageFont.truetype("assets/fonts/Roboto-Medium.ttf", size=20),
        "xp_color": (255, 255, 255)
    },
    "e": {
        "owner": 835374941095460916,
        "description": "nice rank card by Qyin :>",

        "avatar_resize": 215 - 70,
        "avatar_xy": (20, 70),

        "progress_bar_width": 636 - 263 - 4,
        "progress_bar_height": 137 - 121 - 4,
        "progress_bar_start_x": 263 + 2,
        "progress_bar_start_y": 121 + 2,
        "progress_bar_color": (255, 255, 255),

        "username_x": 400,
        "username_y": 5,
        "username_font": ImageFont.truetype("assets/fonts/consolab.ttf", size=30),

        "rank_xy": (355, 155),
        "level_xy": (355, 185),
        "xp_xy": (500, 150),
        "no_xp_text": False,

        "rank_and_level_font": ImageFont.truetype("assets/fonts/consolab.ttf", size=25),
        "xp_font": ImageFont.truetype("assets/fonts/consolab.ttf", size=17),
        "xp_color": (255, 255, 255),
    },
    "clippy": {
        "owner": 561863298887450644,
        "description": "Rankcard by clippy",

        "avatar_resize": 301 - 55,
        "avatar_xy": (40, 63),

        "progress_bar_width": 913 - 334,
        "progress_bar_height": 238 - 227,
        "progress_bar_start_x": 334,
        "progress_bar_start_y": 227,
        "progress_bar_color": (61, 45, 149),

        "username_x": 335,
        "username_y": 150,
        "username_font": ImageFont.truetype("assets/fonts/Roboto-Bold.ttf", size=55),

        "rank_xy": (750, 15),
        "level_xy": (870, 15),
        "xp_xy": (720, 245),
        "no_xp_text": False,

        "rank_and_level_font": ImageFont.truetype("assets/fonts/Roboto-Bold.ttf", size=25),
        "xp_font": ImageFont.truetype("assets/fonts/Roboto-Bold.ttf", size=20),
        "xp_color": (255, 255, 255)
    }
}


class Leveling(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 20, commands.BucketType.user)

    async def set_default_user_level_data(self, user_id, guild_id):
        e = {
            "id": user_id,
            "guild_id": guild_id,
            "xp": 0,
            "messages": 0
        }
        self.client.leveling_cache.append(e)
        return await self.get_user_level_data(user_id, guild_id)

    async def get_user_level_data(self, user_id, guild_id):
        for e in self.client.leveling_cache:
            if e['id'] == user_id and e['guild_id'] == guild_id:
                return e
        return await self.set_default_user_level_data(user_id, guild_id)

    async def process_rank_card(self, template_name, user):
        user_data = await self.get_user_level_data(user.id, user.guild.id)

        t = rank_card_templates[template_name]

        username_color = (255, 255, 255) if "username_color" not in t else t['username_color']
        level_color = (255, 255, 255) if "level_color" not in t else t['level_color']
        xp_color = (211, 211, 211) if "xp_color" not in t else t['xp_color']

        lvl = await get_level(user_data['xp'])
        how_nice = {}

        for e in self.client.leveling_cache:
            if e['guild_id'] == user.guild.id:
                how_nice.update({e['id']: e['xp']})
        yes = dict(sorted(how_nice.items(), key=itemgetter(1), reverse=True))

        rank_template = Image.open(f"assets/images/rank_cards/{template_name}.png")

        # getting avatar
        avatar_asset = user.display_avatar.with_format('png')
        avatar_data = BytesIO(await avatar_asset.read())
        user_avatar = Image.open(avatar_data)
        user_avatar = user_avatar.resize((t['avatar_resize'], t['avatar_resize']))

        # mask for circle avatar
        mask_img = Image.new("L", user_avatar.size, 0)
        draw = ImageDraw.Draw(mask_img)
        draw.ellipse((0, 0, t['avatar_resize'], t['avatar_resize']), fill=255)
        mask_img.save('assets/temp/mask_circle.png')

        # pasting avatar in image
        temp_rank = rank_template.copy()
        temp_rank.paste(user_avatar, t['avatar_xy'], mask_img)

        # progress bar
        draw2 = ImageDraw.Draw(temp_rank)
        draw2.rectangle(
            [
                (t['progress_bar_start_x'], t['progress_bar_start_y']),
                (t['progress_bar_start_x'] + (t['progress_bar_width'] * (user_data['xp'] - ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))) / (
                    200 * ((1 / 2) * lvl))), t['progress_bar_start_y'] + t['progress_bar_height'])
            ],
            fill=t['progress_bar_color']
        )

        # addings text
        draw2.text((t['username_x'], t['username_y']), str(user.name), username_color, font=t['username_font'])  # name

        if "rank_xy" in t:
            draw2.text(t['rank_xy'], f"#{list(yes.keys()).index(user.id) + 1}", (255, 255, 255), font=t['rank_and_level_font'])  # rank
        draw2.text(t['level_xy'], str(lvl), level_color, font=t['rank_and_level_font'])  # level

        # xp text
        draw2.text(
            t['xp_xy'],
            f"{user_data['xp'] - ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))} / {int(200 * ((1 / 2) * lvl))} {'XP' if t['no_xp_text'] == False else ''}",
            xp_color,
            font=t['xp_font']
        )

        temp_rank.save('assets/temp/rank.png')

    @commands.Cog.listener(name="on_message")
    async def add_xp(self, message: Message):
        if message.author.bot:
            return
        if not message.guild:
            return
        guild_config = await self.client.get_guild_config(message.guild.id)
        if not guild_config['leveling']['enabled']:
            return
        bucket = self.cd_mapping.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return
        user_data = await self.get_user_level_data(message.author.id, message.guild.id)
        user_data.update({"xp": user_data['xp'] + 5})
        lvl = await get_level(user_data['xp'])
        if (50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)) == user_data['xp']:

            channel = message.channel if guild_config['leveling']['channel_id'] is None else self.client.get_channel(
                guild_config['leveling']['channel_id'])
            if "message" not in guild_config['leveling']:
                level_up_msg = DEFAULT_LEVEL_UP_MSG
            else:
                level_up_msg = DEFAULT_LEVEL_UP_MSG if guild_config['leveling']['message'] is None else guild_config['leveling']['message']
            mm_msg_yes = await process_level_up_messages(level_up_msg, message.author, lvl, user_data['messages'])
            if channel is None:
                channel = message.channel
            try:
                await channel.send(mm_msg_yes, allowed_mentions=AllowedMentions(
                    everyone=False,
                    roles=False,
                    users=True,
                    replied_user=False
                ))
            except Exception:
                pass

            if "roles" not in guild_config['leveling']:
                return
            if str(lvl) in guild_config['leveling']['roles']:
                role = message.guild.get_role(guild_config['leveling']['roles'][str(lvl)])

                await message.author.add_roles(role, reason="EpicBot level roles!")

            for e in guild_config['leveling']['roles']:
                if int(e) < lvl:
                    role = message.guild.get_role(guild_config['leveling']['roles'][e])

                    await message.author.add_roles(role, reason="EpicBot level roles!")

    @commands.Cog.listener(name="on_message")
    async def add_messages(self, message: Message):
        if message.author.bot:
            return
        if not message.guild:
            return
        guild_config = await self.client.get_guild_config(message.guild.id)
        if not guild_config['leveling']['enabled']:
            return
        user_data = await self.get_user_level_data(message.author.id, message.guild.id)
        user_data.update({"messages": user_data['messages'] + 1})

    @commands.command()
    async def rank_(self, ctx: commands.Context, user: Member = None):
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        prefix = ctx.clean_prefix
        if not guild_config['leveling']['enabled']:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Not enabled!",
                f"Levels are not enabled for this server.\nPlease enable them using `{prefix}leveling enable`"
            ))
        if user is None:
            user = ctx.author
        if user.bot:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} No bots!",
                "Bots do not have any rank."
            ))
        user_profile = await self.client.get_user_profile_(user.id)
        template = user_profile['rank_card_template']

        await self.process_rank_card(template, user)

        return await ctx.reply(file=File('assets/temp/rank.png'))

    @commands.is_owner()
    @commands.command()
    async def rank_from_template(self, ctx, member, template, reply=True):
        await self.process_rank_card(template, member)

        if reply:
            return await ctx.reply(file=File('assets/temp/rank.png'))

    @commands.command()
    @commands.is_owner()
    async def leveling_lb(self, ctx: commands.Context):
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        prefix = ctx.clean_prefix
        if not guild_config['leveling']['enabled']:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Not enabled!",
                f"Levels are not enabled for this server.\nPlease enable them using `{prefix}leveling enable`"
            ))

        how_nice = {}

        for e in self.client.leveling_cache:
            if e['guild_id'] == ctx.guild.id:
                how_nice.update({e['id']: e['xp']})

        yes = dict(sorted(how_nice.items(), key=itemgetter(1), reverse=True))

        e = ""
        i = 1

        for h in yes:
            if i > 10:
                break
            lvl = await get_level(yes[h])
            e += f"`{str(i) + ('. ' if i != 10 else '.')}` <@{h}> • Level `{lvl}` (`{yes[h] - ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))}` / `{int(200*((1/2)*lvl))}` XP)\n"
            i += 1

        embed = Embed(
            title=f"{EMOJIS['leveling']} Levels leaderboard!",
            description=e,
            color=MAIN_COLOR
        )

        await ctx.reply(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def messages_lb(self, ctx: commands.Context):
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        prefix = ctx.clean_prefix
        if not guild_config['leveling']['enabled']:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Not enabled!",
                f"Levels are not enabled for this server.\nPlease enable them using `{prefix}leveling enable`"
            ))

        how_nice = {}

        for e in self.client.leveling_cache:
            if e['guild_id'] == ctx.guild.id:
                how_nice.update({e['id']: e['messages']})

        yes = dict(sorted(how_nice.items(), key=itemgetter(1), reverse=True))

        e = ""
        i = 1

        for h in yes:
            if i > 10:
                break
            e += f"`{str(i) + ('. ' if i != 10 else '.')}` <@{h}> • `{yes[h]}` messages\n"
            i += 1

        embed = Embed(
            title="📬  Messages leaderboard!",
            description=e,
            color=MAIN_COLOR
        )

        await ctx.reply(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def messages_(self, ctx: commands.Context, user: Member = None):
        guild_config = await self.client.get_guild_config(ctx.guild.id)
        prefix = ctx.clean_prefix
        if not guild_config['leveling']['enabled']:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Not enabled!",
                f"Levels are not enabled for this server.\nPlease enable them using `{prefix}leveling enable`"
            ))
        if user is None:
            user = ctx.author
        if user.bot:
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} No bots!",
                "Bot messages are not counted."
            ))
        user_data = await self.get_user_level_data(user.id, ctx.guild.id)

        return await ctx.reply(embed=success_embed(
            "📬  Messages",
            f"**{escape_markdown(str(user))}** has `{user_data['messages']}` messages!"
        ))


def setup(client):
    client.add_cog(Leveling(client))

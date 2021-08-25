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

import asyncio
import validators
import json as json_but_pain

from discord import Embed
from config import MAIN_COLOR, RED_COLOR


def success_embed(title, description):
    return Embed(
        title=title,
        description=description,
        color=MAIN_COLOR
    )


def meh_embed(title, description):
    return Embed(
        title=title,
        description=description
    )


def error_embed(title, description):
    return Embed(
        title=title,
        description=description,
        color=RED_COLOR
    )


async def edit_msg_multiple_times(ctx, time_, first_msg, other_msgs, final_emb):
    msg = await ctx.send(embed=Embed(title=first_msg, color=MAIN_COLOR))
    await asyncio.sleep(time_)

    for e in other_msgs:
        embed = Embed(title=e[0], color=MAIN_COLOR)
        if len(e) == 2:
            embed.description = e[1]
        await msg.edit(embed=embed)
        await asyncio.sleep(time_)

    await msg.edit(embed=final_emb)


async def replace_things_in_string_fancy_lemao(bot, array, string_):
    author = array[0]
    guild = array[1]
    inviter_id = await bot.get_inviter(author.id, guild.id)

    if inviter_id == 'Unknown':
        inviter_name = 'Unknown'
        inviter_discrim = 'Unknown'
        inviter_tag = 'Unknown'
        inviter_id_ = 'Unknown'
        inviter_mention = 'Unknown'
        inviter_avatar = 'https://cdn.discordapp.com/embed/avatars/1.png'
        inviter_invites = 'Unknown'
    else:
        inviter__ = bot.get_user(inviter_id)
        inviter_name = 'Unknown' if inviter__ is None else inviter__.name
        inviter_discrim = 'Unknown' if inviter__ is None else inviter__.discriminator
        inviter_tag = 'Unknown' if inviter__ is None else inviter_name + '#' + inviter_discrim
        inviter_id_ = 'Unknown' if inviter__ is None else inviter__.id
        inviter_mention = 'Unknown' if inviter__ is None else inviter__.mention
        inviter_avatar = 'https://cdn.discordapp.com/embed/avatars/1.png' if inviter__ is None else inviter__.display_avatar.url
        inviter_invites = 'Unknown' if inviter__ is None else await bot.fetch_invites(inviter_id_, guild.id)

    nice = {
        "{user_name}": author.name,
        "{user_nickname}": author.display_name,
        "{user_discrim}": str(author.discriminator),
        "{user_tag}": author.name + '#' + str(author.discriminator),
        "{user_id}": author.id,
        "{user_mention}": author.mention,
        "{user_avatar}": author.display_avatar.url,

        "{guild_name}": guild.name,
        "{guild_id}": guild.id,
        "{guild_membercount}": guild.member_count,
        "{guild_icon}": guild.icon.url if guild.icon is not None else 'https://cdn.discordapp.com/embed/avatars/1.png',
        "{guild_owner_name}": guild.owner.name,
        "{guild_owner_id}": guild.owner_id,
        "{guild_owner_mention}": guild.owner.mention,

        "{user_invites}": await bot.fetch_invites(author.id, guild.id),
        "{inviter_name}": inviter_name,
        "{inviter_discrim}": inviter_discrim,
        "{inviter_tag}": inviter_tag,
        "{inviter_id}": inviter_id_,
        "{inviter_mention}": inviter_mention,
        "{inviter_avatar}": inviter_avatar,
        "{inviter_invites}": inviter_invites,

        "\\": "\\\\",
    }

    for i, j in nice.items():
        string_ = string_.replace(i, str(j))
    return string_


async def process_embeds_from_json(bot, array, json, replace: bool = True):
    embed = Embed()

    if replace:
        poggers = await replace_things_in_string_fancy_lemao(bot, array, json_but_pain.dumps(json))
        uwu_json = json_but_pain.loads(poggers)
    else:
        uwu_json = json

    content = None if "plainText" not in json else uwu_json['plainText']

    embed_title = None if "title" not in json else uwu_json['title']
    embed_url = None if "url" not in json else uwu_json['url']
    embed_desc = None if "description" not in json else uwu_json['description']
    embed_image = None if "image" not in json else uwu_json['image']
    embed_thumbnail = None if "thumbnail" not in json else uwu_json['thumbnail']
    embed_color = None if "color" not in json else uwu_json['color']
    field_count = 0

    if embed_color == "MAIN_COLOR":
        embed_color = MAIN_COLOR
    if embed_color == "RED_COLOR":
        embed_color = RED_COLOR

    embed_author = {}
    embed_footer = {}

    if "author" in json:
        if "name" not in uwu_json['author']:
            return 'pain author name'
        embed_author.update({
            "name": uwu_json['author']['name'],
            "url": None if "url" not in uwu_json['author'] else uwu_json['author']['url'],
            "icon_url": None if "icon_url" not in uwu_json['author'] else uwu_json['author']['icon_url']
        })
    if "footer" in json:
        if "text" not in uwu_json['footer']:
            return 'pain footer text'
        embed_footer.update({
            "text": uwu_json['footer']['text'],
            "icon_url": None if "icon_url" not in uwu_json['footer'] else uwu_json['footer']['icon_url']
        })
    if "fields" in json:
        for e in uwu_json['fields']:
            if e['name'] != "" and e['value'] != "":
                embed.add_field(
                    name=e['name'],
                    value=e['value'],
                    inline=e['inline']
                )
                field_count += 1
            else:
                return 'pain empty fields'

    if embed_title is not None:
        embed.title = embed_title
    if embed_desc is not None:
        embed.description = embed_desc
    if embed_url is not None:
        embed.url = embed_url
    if embed_image is not None:
        embed.set_image(url=embed_image)
    if embed_thumbnail is not None:
        embed.set_thumbnail(url=embed_thumbnail)
    if embed_color is not None:
        embed.color = embed_color

    if len(embed_author) != 0:
        if embed_author['url'] is None and embed_author['icon_url'] is None:
            embed.set_author(name=embed_author['name'])
        elif embed_author['url'] is None and embed_author['icon_url'] is not None:
            embed.set_author(name=embed_author['name'], icon_url=embed_author['icon_url'])
        elif embed_author['url'] is not None and embed_author['icon_url'] is None:
            embed.set_author(name=embed_author['name'], url=embed_author['url'])
        else:
            embed.set_author(name=embed_author['name'], url=embed_author['url'], icon_url=embed_author['icon_url'])

    if len(embed_footer) != 0:
        if embed_footer['icon_url'] is None:
            embed.set_footer(text=embed_footer['text'])
        else:
            embed.set_footer(text=embed_footer['text'], icon_url=embed_footer['icon_url'])

    if (embed_url is not None and not validators.url(embed_url)) or (embed_image is not None and not validators.url(embed_image)) or (embed_thumbnail is not None and not validators.url(embed_thumbnail)):
        return 'pain invalid urls'
    if len(embed_author) != 0:
        if embed_author['url'] is not None and not validators.url(embed_author['url']):
            return 'pain invalid urls'
        if embed_author['icon_url'] is not None and not validators.url(embed_author['icon_url']):
            return 'pain invalid urls'
    if len(embed_footer) != 0:
        if embed_footer['icon_url'] is not None and not validators.url(embed_footer['icon_url']):
            return 'pain invalid urls'

    if embed_title is None and embed_desc is None and len(embed_author) == 0 and len(embed_footer) == 0 and field_count == 0 and embed_image is None:
        return 'pain empty embed'

    return [content, embed]

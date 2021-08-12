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
import discord
import aiohttp

from discord.ext import commands, tasks
from twitchAPI.twitch import Twitch
from config import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, EMOJIS
from utils.bot import EpicBot

twitch = Twitch(TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET)
twitch.authenticate_app([])
TWITCH_STREAM_API_ENDPOINT_V5 = "https://api.twitch.tv/kraken/streams/{}"
API_HEADERS = {
    'Client-ID': TWITCH_CLIENT_ID,
    'Accept': 'application/vnd.twitchtv.v5+json',
}


class TwitchNotifs(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client
        self.live_notifs_loop.start()

    async def check_live_user(self, user):
        try:
            userid = twitch.get_users(logins=[user])['data'][0]['id']
            url = TWITCH_STREAM_API_ENDPOINT_V5.format(userid)
            try:
                async with aiohttp.ClientSession() as s:
                    async with s.get(url, headers=API_HEADERS) as r:
                        jsondata = await r.json()
                        if 'stream' in jsondata:
                            if jsondata['stream'] is not None:
                                return jsondata['stream']
                            else:
                                return False
            except Exception as e:
                print("Error in twitch for user: ", e)
                return False
        except IndexError:
            return False

    @tasks.loop(minutes=2)
    async def live_notifs_loop(self):
        await self.client.wait_until_ready()
        for e in self.client.serverconfig_cache:
            if e['twitch']['username'] is not None and e['twitch']['channel_id'] is not None:
                channel = self.client.get_channel(e['twitch']['channel_id'])
                if channel is not None:
                    try:
                        status = await self.check_live_user(e['twitch']['username'])
                        await asyncio.sleep(1)
                        if not status and not e['twitch']['currently_live']:
                            e['twitch'].update({"currently_live": True})
                            nice = "**🎮  Game:** " + status['game'] + '\n'
                            nice += "**" + EMOJIS['members'] + "  Viewers:** " + str(status['viewers']) + '\n'
                            nice += "**" + EMOJIS['ramaziHeart'] + "  Followers:** " + str(status['channel']['followers']) + '\n'
                            embed = discord.Embed(
                                title=status['channel']['status'],
                                description=nice,
                                url=f"https://twitch.tv/{e['twitch']['username']}",
                                color=0x9147fe
                            )
                            embed.set_thumbnail(url=status['channel']['logo'])
                            embed.set_image(url=status['preview']['large'])
                            embed.set_author(name=e['twitch']['username'], icon_url=status['channel']['logo'], url=f"https://twitch.tv/{e['twitch']['username']}")
                            await channel.send(
                                f"Poggers! **{e['twitch']['username']}** is now live! Go check them out! <https://twitch.tv/{e['twitch']['username']}>" if e['twitch']['message'] is None else e['twitch']['message'].replace(
                                    "{streamer}",
                                    f"**{e['twitch']['username']}**"
                                ).replace(
                                    "{url}",
                                    "<https://twitch.tv/" + e['twitch']['username'] + ">"
                                ),
                                embed=embed,
                                allowed_mentions=discord.AllowedMentions.all()
                            )
                        elif not status:
                            e['twitch'].update({"currently_live": False})
                    except Exception:
                        pass


def setup(client):
    client.add_cog(TwitchNotifs(client))

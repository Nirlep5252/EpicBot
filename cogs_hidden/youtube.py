import functools
from discord.ext import commands, tasks
from utils.bot import EpicBot
from pyyoutube import Api, Channel
from config import YOUTUBE_API_KEY
from typing import Union

api = Api(api_key=YOUTUBE_API_KEY)


async def check_new_video(yt_channel_id: str):
    yt_channel = api.get_channel_info(channel_id=yt_channel_id)


async def get_yt_channel(bot: EpicBot, query: str) -> Union[Channel, None]:
    """
    Returns the channel if found or None
    """
    thing = functools.partial(api.get_channel_info, channel_id=query)
    channel_by_id = await bot.loop.run_in_executor(None, thing)
    channel_dict = channel_by_id.to_dict()
    if not channel_dict.get('items'):
        thing = functools.partial(api.get_channel_info, channel_name=query)
        channel_by_search = await bot.loop.run_in_executor(None, thing)
        channel_dict = channel_by_search.to_dict()
        if not channel_dict.get('items'):
            return None
        else:
            return channel_by_search.items[0]
    else:
        return channel_by_id.items[0]


class YouTube(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client

    # @tasks.loop(seconds=300)
    # async def youtube_notifs(self):
    #     for config in self.client.serverconfig_cache:
    #         youtube_config = config.get('youtube', {})
    #         if youtube_config.get('channel_id', None) is not None:
    #             channel = self.client.get_channel(youtube_config['channel_id'])
    #             yt_channel = await get_yt_channel(self.client, youtube_config['youtube_id'])


def setup(client: EpicBot):
    client.add_cog(YouTube(client))

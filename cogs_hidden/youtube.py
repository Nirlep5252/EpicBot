import functools
import discord
import traceback
import asyncio

from discord.ext import commands, tasks
from utils.bot import EpicBot
from pyyoutube import Api, Channel, Video, VideoListResponse, PlaylistItemListResponse
from config import YOUTUBE_API_KEY, ERROR_LOG_CHANNEL
from utils.constants import DEFAULT_YOUTUBE_MSG
from typing import Optional

api = Api(api_key=YOUTUBE_API_KEY)


async def check_new_video(bot: EpicBot, yt_channel_id: str, stored_vid_id: Optional[str] = None) -> Optional[Video]:
    """
    Checks for the last uploaded video, returns None if no new video, else it'll return the video info
    """
    latest_vid_id = await get_playlist_last_vid_id(bot, yt_channel_id.replace("UC", "UU", 1))
    if not latest_vid_id:
        return None
    if latest_vid_id == stored_vid_id:
        return None
    return await get_video_info(bot, latest_vid_id)


async def get_playlist_last_vid_id(bot: EpicBot, query: str) -> Optional[str]:
    thing = functools.partial(api.get_playlist_items, playlist_id=query)
    playlist_by_id: PlaylistItemListResponse = await bot.loop.run_in_executor(None, thing)
    if not playlist_by_id:
        return None
    if not playlist_by_id.items:
        return None
    if not playlist_by_id.items[0].snippet:
        return None
    if not playlist_by_id.items[0].snippet.resourceId:
        return None
    return playlist_by_id.items[0].snippet.resourceId.videoId


async def get_yt_channel(bot: EpicBot, query: str) -> Optional[Channel]:
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


async def get_video_info(bot: EpicBot, query: str) -> Optional[Video]:
    thing = functools.partial(api.get_video_by_id, video_id=query)
    video_list_res: VideoListResponse = await bot.loop.run_in_executor(None, thing)
    if not video_list_res:
        return None
    if not video_list_res.items:
        return None
    return video_list_res.items[0]


def format_yt_msg(text: str, video: Video, channel: Channel) -> str:
    stuff = {
        "{channel_name}": channel.snippet.title,
        "{channel_id}": channel.id,
        "{channel_subs}": channel.statistics.subscriberCount,
        "{video_url}": f"https://youtube.com/watch?v={video.id}",
        "{video_id}": video.id,
        "{video_likes}": video.statistics.likeCount,
        "{video_dislikes}": video.statistics.dislikeCount,
        "{video_views}": video.statistics.viewCount,
        "{video_title}": video.snippet.title,
    }
    for to_replace, replacement in stuff.items():
        text = text.replace(to_replace, replacement)
    return text


class YouTube(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client
        self.youtube_notifs.start()

    @tasks.loop(seconds=600)
    async def youtube_notifs(self):
        for config in self.client.serverconfig_cache:
            try:
                yt_config: dict = config.get('youtube', {})
                if yt_config.get('channel_id') is not None:
                    channel = self.client.get_channel(yt_config['channel_id'])
                    yt_channel = await get_yt_channel(self.client, yt_config.get('youtube_id'))
                    if channel is not None and yt_channel is not None:
                        new_video = await check_new_video(self.client, yt_config.get('youtube_id'), yt_config.get('last_vid'))
                        if new_video is not None:
                            await channel.send(format_yt_msg((yt_config.get('message') or DEFAULT_YOUTUBE_MSG), new_video, yt_channel), allowed_mentions=discord.AllowedMentions.all())
                            yt_config.update({"last_vid": new_video.id})
                            await asyncio.sleep(2)
            except Exception as e:
                error_text = "".join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
                try:
                    await self.client.get_channel(ERROR_LOG_CHANNEL).send(f"Error in youtube loop:```py\n{error_text}\n```")
                except Exception:
                    await self.client.get_channel(ERROR_LOG_CHANNEL).send(f"Error in youtube loop: {e}\n\ncheck console for more details.")
                    print(error_text)

    def cog_unload(self) -> None:
        self.youtube_notifs.stop()


def setup(client: EpicBot):
    client.add_cog(YouTube(client))

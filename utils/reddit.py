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
import aiohttp
import random
from config import MAIN_COLOR


async def check_for_images(url, subreddit, embed_title):
    if ".png" in url or ".jpg" in url:
        return discord.Embed(title=embed_title, color=MAIN_COLOR).set_image(url=url)
    else:
        await pick_random_url_from_reddit(subreddit, embed_title)


async def pick_random_url_from_reddit(subreddit, embed_title):
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'https://www.reddit.com/r/{subreddit}/new.json?sort=hot') as r:
            res = await r.json()
            try:
                url = res['data']['children'][random.randint(0, 20)]['data']['url']
            except IndexError:
                return pick_random_url_from_reddit(subreddit, embed_title)
            return await check_for_images(url, subreddit, embed_title)

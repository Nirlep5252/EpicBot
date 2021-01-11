import discord
import praw
import random
import os
import requests
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import (CommandOnCooldown)
from discord.ext import commands

reddit = praw.Reddit(client_id = os.environ.get("REDDIT_CLIENT_ID"),
                        client_secret = os.environ.get("REDDIT_CLIENT_SECRET"),
                        username = os.environ.get("REDDIT_USERNAME"),
                        password = os.environ.get("REDDIT_PASSWORD"),
                        user_agent = os.environ.get("REDDIT_USER_AGENT"))

class Reddit(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def meme(self, ctx):
        subreddit = reddit.subreddit("memes")
        all_subs = []

        top = subreddit.top(limit = 50)

        for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url

        embed = discord.Embed(title = name, color = 0x00FF0C)
        embed.set_image(url = url)
        await ctx.send(embed = embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def anime(self, ctx):
        response = requests.get("https://shiro.gg/api/images/neko")

        realResponse = response.json()

        embed = discord.Embed(
            title = "uwu",
            color = 0xFFC0CB
        )
        embed.set_image(url = realResponse['url'])

        await ctx.send(embed = embed)
        # subreddit = reddit.subreddit("awwnime")
        # all_subs = []
        #
        # subreddit2 = reddit.subreddit("imaginarysliceoflife")
        # all_subs2 = []
        #
        # subreddit3 = reddit.subreddit("smugs")
        # all_subs3 = []
        #
        # subreddit4 = reddit.subreddit("touchfluffytail")
        # all_subs4 = []
        #
        # subreddit5 = reddit.subreddit("zettairyouiki")
        # all_subs5 = []
        #
        # subreddit6 = reddit.subreddit("Animewallpaper")
        # all_subs6 = []
        #
        # top = subreddit.top(limit = 50)
        # top2 = subreddit2.top(limit = 50)
        # top3 = subreddit3.top(limit = 50)
        # top4 = subreddit4.top(limit = 50)
        # top5 = subreddit5.top(limit = 50)
        # top6 = subreddit6.top(limit = 50)
        #
        # for submission in top:
        #     all_subs.append(submission)
        #
        # for submission2 in top2:
        #     all_subs2.append(submission2)
        #
        # for submission3 in top3:
        #     all_subs3.append(submission3)
        #
        # for submission4 in top4:
        #     all_subs4.append(submission4)
        #
        # for submission5 in top5:
        #     all_subs5.append(submission5)
        #
        # for submission6 in top6:
        #     all_subs6.append(submission6)
        #
        # random_sub = random.choice(all_subs)
        # random_sub2 = random.choice(all_subs2)
        # random_sub3 = random.choice(all_subs3)
        # random_sub4 = random.choice(all_subs4)
        # random_sub5 = random.choice(all_subs5)
        # random_sub6 = random.choice(all_subs6)
        #
        # random_random_sub = [random_sub, random_sub2, random_sub3, random_sub4, random_sub5, random_sub6]
        #
        # big_boi_random_sub = random.choice(random_random_sub)
        #
        # url = big_boi_random_sub.url
        #
        # embed = discord.Embed(color = 0x00FF0C)
        # embed.set_image(url = url)
        #
        # await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Reddit(client))

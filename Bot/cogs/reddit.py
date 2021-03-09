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

def setup(client):
    client.add_cog(Reddit(client))

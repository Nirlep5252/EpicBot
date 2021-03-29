import discord
import requests
import aiohttp
from discord.ext import commands
from config import *


class Images(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def meme(self, ctx):
        embed=discord.Embed(
            title = "Haha!",
            color = MAIN_COLOR
        )

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def anime(self, ctx):
        response = requests.get("https://shiro.gg/api/images/neko")

        realResponse = response.json()

        embed = discord.Embed(
            title="uwu",
            color=PINK_COLOR_2
        )
        embed.set_image(url=realResponse['url'])

        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['meow', 'cats'])
    async def cat(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r:
                    data = await r.json()

                    embed = discord.Embed(
                        title="Meow! <:CBCattoHuggo:825638003753877504>", color=MAIN_COLOR)
                    embed.set_image(url=data['file'])

                    await ctx.message.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['dogs'])
    async def dog(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://random.dog/woof.json") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Woof!", color=MAIN_COLOR)
                    embed.set_image(url=data['url'])

                    await ctx.message.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def fox(self, ctx):
        url = "https://randomfox.ca/floof/"
        response = requests.get(url)
        fox = response.json()

        embed = discord.Embed(color=MAIN_COLOR)
        embed.set_image(url=fox['image'])
        await ctx.message.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def panda(self, ctx):
        url = 'https://some-random-api.ml/img/panda'
        response = requests.get(url)
        img = response.json()

        embed = discord.Embed(title="Panda 🐼", color=MAIN_COLOR)
        embed.set_image(url=img['link'])
        await ctx.message.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def redpanda(self, ctx):
        url = 'https://some-random-api.ml/img/red_panda'
        response = requests.get(url)
        img = response.json()

        embed = discord.Embed(title="Red Panda", color=MAIN_COLOR)
        embed.set_image(url=img['link'])
        await ctx.message.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['pika'])
    async def pikachu(self, ctx):
        url = 'https://some-random-api.ml/img/pikachu'
        response = requests.get(url)
        img = response.json()

        embed = discord.Embed(title="Pika!", color=MAIN_COLOR)
        embed.set_image(url=img['link'])
        await ctx.message.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def comment(self, ctx, *, msg=None):
        if msg == None:
            await ctx.message.reply(embed=discord.Embed(
                title="Error!",
                description=f"Incorrect Usage! Use like this: `e!comment <text>`",
                color=RED_COLOR
            ))
            return
        url = f"https://some-random-api.ml/canvas/youtube-comment?avatar={ctx.author.avatar_url}&username={ctx.author.name}&comment={msg}"
        url = url.replace(" ", "%20")
        embed = discord.Embed(color=MAIN_COLOR)
        embed.set_image(url=url)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def wasted(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        url = f"https://some-random-api.ml/canvas/wasted?avatar={user.avatar_url}"
        embed = discord.Embed(color=MAIN_COLOR)
        embed.set_image(url=url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Images(client))

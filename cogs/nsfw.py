import discord
import requests
import datetime
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import (CommandOnCooldown)
from discord.ext import commands


class NSFW(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def hentai(self, ctx):
        if ctx.channel.id == 768722875972452352:
            await ctx.send("No.")
            return
        if ctx.channel.is_nsfw():
            response = requests.get("https://shiro.gg/api/images/nsfw/hentai")

            realResponse = response.json()

            embed = discord.Embed(
                title = "There you go!",
                color = 0xFFC0CB
            )
            embed.set_image(url = realResponse['url'])

            await ctx.message.reply(embed = embed)
        else:
            await ctx.message.reply("This command can only be used in a NSFW channel.")
            
            
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def hentai(self, ctx):
        if ctx.channel.id == 768722875972452352:
            await ctx.send("No.")
            return
        if ctx.channel.is_nsfw():
            response = requests.get("https://nekos.life/api/v2/img/cum")

            realResponse = response.json()

            embed = discord.Embed(
                title = "There you go!",
                color = 0xFFC0CB
            )
            embed.set_image(url = realResponse['url'])

            await ctx.message.reply(embed = embed)
        else:
            await ctx.message.reply("This command can only be used in a NSFW channel.")

   

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def thighs(self, ctx):
        if ctx.channel.id == 768722875972452352:
            await ctx.send("No.")
            return
        if ctx.channel.is_nsfw():
            response = requests.get("https://shiro.gg/api/images/nsfw/thighs")

            realResponse = response.json()

            embed = discord.Embed(
                title = "Thighs!",
                color = 0xFFC0CB
            )
            embed.set_image(url = realResponse['url'])

            await ctx.message.reply(embed = embed)
        else:
            await ctx.message.reply("This command can only be used in a NSFW channel.")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def nekogif(self, ctx):
        if ctx.channel.id == 768722875972452352:
            await ctx.send("No.")
            return
        if ctx.channel.is_nsfw():
            response = requests.get("https://nekos.life/api/v2/img/nsfw_neko_gif")

            realResponse = response.json()

            embed = discord.Embed(
                title = "Gifs!",
                color = 0xFFC0CB
            )
            embed.set_image(url = realResponse['url'])

            await ctx.message.reply(embed = embed)
        else:
            await ctx.message.reply("This command can only be used in a NSFW channel.")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def boobs(self, ctx):
        if ctx.channel.id == 768722875972452352:
            await ctx.send("No.")
            return
        if ctx.channel.is_nsfw():
            response = requests.get("https://nekos.life/api/v2/img/boobs")

            realResponse = response.json()

            embed = discord.Embed(
                title = "boooooobs!",
                color = 0xFFC0CB
            )
            embed.set_image(url = realResponse['url'])

            await ctx.message.reply(embed = embed)
        else:
            await ctx.message.reply("This command can only be used in a NSFW channel.")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def blowjob(self, ctx):
        if ctx.channel.id == 768722875972452352:
            await ctx.send("No.")
            return
        if ctx.channel.is_nsfw():
            response = requests.get("https://nekos.life/api/v2/img/blowjob")

            realResponse = response.json()

            embed = discord.Embed(
                title = "Yummy!",
                color = 0xFFC0CB
            )
            embed.set_image(url = realResponse['url'])

            await ctx.message.reply(embed = embed)
        else:
            await ctx.message.reply("This command can only be used in a NSFW channel.")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def pussy(self, ctx):
        if ctx.channel.id == 768722875972452352:
            await ctx.send("No.")
            return
        if ctx.channel.is_nsfw():
            response = requests.get("https://nekos.life/api/v2/img/pussy")

            realResponse = response.json()

            embed = discord.Embed(
                title = "Yummy!",
                color = 0xFFC0CB
            )
            embed.set_image(url = realResponse['url'])

            await ctx.message.reply(embed = embed)
        else:
            await ctx.message.reply("This command can only be used in a NSFW channel.")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def spank(self, ctx, user: discord.Member = None):
        if ctx.channel.id == 768722875972452352:
            await ctx.send("No.")
            return
        if ctx.channel.is_nsfw():
            if user == None:
                await ctx.message.reply("Who do you want to spank? Mention them next time idiot.")
                return

            if user == ctx.author:
                await ctx.message.reply("How lonely are you? Don't spank yourself!")
                return

            response = requests.get("https://nekos.life/api/v2/img/spank").json()

            embed = discord.Embed(
                title = "Damn!",
                description = f"{user.mention} got spanked by {ctx.author.mention}",
                color = 0xFFC0CB
            )
            embed.set_image(url = response['url'])
            await ctx.message.reply(embed = embed)
        else:
            await ctx.message.reply("This command can only be used in a NSFW channel.")

def setup(client):
    client.add_cog(NSFW(client))

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

from discord.ext import commands
from discord.utils import escape_markdown
from utils.bot import EpicBot
from utils.embed import error_embed
from config import EMOJIS, PINK_COLOR


class nsfw(commands.Cog, description="Oh boi..."):
    def __init__(self, client: EpicBot):
        self.client = client

    async def get_image_from_api(self, url, thing):
        async with self.client.session.get(url) as r:
            uwu = await r.json()
            image = uwu[thing]
            return discord.Embed(color=PINK_COLOR).set_image(url=image)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.is_nsfw()
    @commands.command(help="Fuck someone!")
    async def fuck(self, ctx: commands.Context, user: discord.Member = None):
        if user is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed("Bruh!", "Who do you want to fuck? Mention them next time idiot."))
        if user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed("Bruh!", "How lonely are you? Don't fuck yourself!"))
        if user.bot:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed("Bruh!", "You can't fuck bots!"))
        embed = await self.get_image_from_api("https://purrbot.site/api/img/nsfw/fuck/gif", "link")
        embed.title = "Wowie!"
        embed.description = f"**{escape_markdown(str(user.name))}** got fucked hard by **{escape_markdown(str(ctx.author.name))}**"
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.is_nsfw()
    @commands.command(help="Cum inside someone ><")
    async def cum(self, ctx: commands.Context, user: discord.Member = None):
        if user is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed("Bruh!", "Who do you want to cum inside? Mention them next time idiot."))
        if user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed("Bruh!", "How lonely are you? Don't cum inside yourself!"))
        if user.bot:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed("Bruh!", "You can't cum inside bots!"))
        embed = await self.get_image_from_api("https://nekos.life/api/v2/img/cum", "url")
        embed.title = f"Mmmm {EMOJIS['mmm']}"
        embed.description = f"**{escape_markdown(str(ctx.author.name))}** cummed inside **{escape_markdown(str(user.name))}**"
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.is_nsfw()
    @commands.command(help="Someones being naughty? Spank them!")
    async def spank(self, ctx: commands.Context, user: discord.Member = None):
        if user is None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed("Bruh!", "Who do you want to spank? Mention them next time idiot."))
        if user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed("Bruh!", "How lonely are you? Don't spank yourself!"))
        if user.bot:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed("Bruh!", "You can't spank bots!"))
        embed = await self.get_image_from_api("https://nekos.life/api/v2/img/spank", "url")
        embed.title = "Damn!"
        embed.description = f"**{escape_markdown(str(ctx.author.name))}** spanked **{escape_markdown(str(user.name))}**"
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.is_nsfw()
    @commands.command(help="Hentai...")
    async def hentai(self, ctx: commands.Context):
        embed = await self.get_image_from_api("https://shiro.gg/api/images/nsfw/hentai", "url")
        embed.title = "There you go!"
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.is_nsfw()
    @commands.command(help="Thighs...")
    async def thighs(self, ctx: commands.Context):
        embed = await self.get_image_from_api("https://shiro.gg/api/images/nsfw/thighs", "url")
        embed.title = "Yummy!!"
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.is_nsfw()
    @commands.command(help="Nekos but NSFW gifs...")
    async def nekogif(self, ctx: commands.Context):
        embed = await self.get_image_from_api("https://nekos.life/api/v2/img/nsfw_neko_gif", "url")
        embed.title = "Gifs!"
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.is_nsfw()
    @commands.command(help="Boobs...")
    async def boobs(self, ctx: commands.Context):
        embed = await self.get_image_from_api("https://nekos.life/api/v2/img/boobs", "url")
        embed.title = "Boooooobs! :D"
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.is_nsfw()
    @commands.command(help="Blowjob...")
    async def blowjob(self, ctx: commands.Context):
        embed = await self.get_image_from_api("https://nekos.life/api/v2/img/blowjob", "url")
        embed.title = "Yummy! 😋"
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.is_nsfw()
    @commands.command(help="Pussies...")
    async def pussy(self, ctx: commands.Context):
        embed = await self.get_image_from_api("https://nekos.life/api/v2/img/pussy", "url")
        embed.title = "Yummy! 😋"
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(nsfw(client))

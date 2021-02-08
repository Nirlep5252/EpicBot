import discord 
import requests 
from discord.ext import commands 

class Actions(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.command()
	async def hug(self, ctx, user: discord.User = None):
		if user == None:
			await ctx.message.reply(f"Why are you so lonely? Mention someone that you wanna hug, you can't hug yourself :(")
			return

		embed = discord.Embed(
			title = "aww hugs uwu",
			description = "this is so cute ><",
			color = 0xFFC0CB
			)
		embed.set_image(url=requests.get("https://nekos.life/api/hug").json()['url'])

		await ctx.send(embed = embed)

	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.command()
	async def kiss(self, ctx, user: discord.User = None):
		if user == None:
			await ctx.message.reply(f"Why are you so lonely? Mention someone that you wanna kiss, you can't kiss yourself :(")
			return

		embed = discord.Embed(
			title = "<a:kissr:808235262261723156><a:kissl:808235261708337182>",
			description = f"{ctx.author.mention} just kissed {user.mention}",
			color = 0xFFC0CB
			)
		embed.set_image(url=requests.get("https://nekos.life/api/kiss").json()['url'])

		await ctx.send(embed=embed)

	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.command()
	async def pat(self, ctx, user: discord.User = None):
		if user == None:
			await ctx.message.reply(f"Why are you so lonely? Mention someone that you wanna pat, you can't pat yourself :(")
			return

		embed = discord.Embed(
			title = "*cute pats*",
			description = f"<a:uwuAYAYA:800611977247719424>",
			color = 0xFFC0CB
			)
		embed.set_image(url=requests.get("https://nekos.life/api/pat").json()['url'])

		await ctx.send(embed=embed)

def setup(client):
	client.add_cog(Actions(client))
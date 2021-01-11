import discord
import inspect
from discord.ext import commands

class Eval(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *,msg = None):
        if ctx.author.id != 558861606063308822:
            await ctx.send("You can't use this cmd bruh.")
            return
        if msg == None:
            await ctx.send("Bruh enter something lol")
        try:
            res = eval(msg)
            if inspect.isawaitable(res):
                await ctx.send(await res)
            else:
                await ctx.send(res)
        except Exception as e:
            print(e)
            await ctx.send(f"ERROR: {e}")

def setup(client):
    client.add_cog(Eval(client))

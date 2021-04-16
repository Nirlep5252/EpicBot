import discord
import inspect
from discord.ext import commands

class Eval(commands.Cog):
    def __init__(self, client):
        self.client = client

    # jsk py is better i recommend not using this shit

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *,msg = None):
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
            await ctx.send(f"**Error**: `{e}`")

def setup(client):
    client.add_cog(Eval(client))

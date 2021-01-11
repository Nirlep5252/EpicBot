import discord
from discord.ext import commands

class Replys(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.command()
    # async def reply(self, ctx, *,message = None):
    #     filter = ['@here', '@everyone']
    #
    #     if message == None:
    #         await ctx.message.reply(f"Please enter a message that you want me to reply with.")
    #         return
    #
    #     for word in filter:
    #         if message.count(word) > 0:
    #             await ctx.message.reply(f"Sorry, I won't ping everyone. Try something else.")
    #             return
    #
    #     await ctx.message.reply(message)

def setup(client):
    client.add_cog(Replys(client))

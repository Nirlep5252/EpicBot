import discord
import asyncio
import datetime
from discord.ext import commands

class SelfDestruct(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['selfdestruct', 'timed_message', 'timedmessage', 'timed_msg', 'timedmsg'])
    @commands.has_permissions(manage_guild = True)
    async def self_destruct(self, ctx, textChannel: discord.TextChannel = None, time = None, *, message = None):
        if time == None or message == None or  textChannel == None:
            await ctx.send(f"Please enter all the parameters. Example: `e!selfdestruct <text channel> <time> <message>`")
            return

        def convert(time):
            pos = ["s", "m", "h", "d"]

            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}

            unit = time[-1]

            if unit not in pos:
                return -1
            try:
                val = int(time[:-1])
            except:
                return -2

            return val * time_dict[unit]

        realTime = convert(time)

        if realTime == -1:
            await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time.")
            return
        elif realTime == -2:
            await ctx.send(f"The time must be an integer. Please enter an interger next time.")
            return

        embed = discord.Embed(title = "Timed Message", description = message, color = 0x00FFFF)
        embed.set_author(name = ctx.author.name, icon_url = ctx.author.avatar_url)
        embed.set_footer(text=f"Get deleted after {time}.", icon_url=f"{ctx.author.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

        try:
            msg = await textChannel.send(embed = embed)
            await ctx.send(f"The timed message has been sent in {textChannel.mention} and will self destruct itself in `{time}` time.")
        except:
            await ctx.send(f"I wasn't able to send the message in {textChannel.mention}, maybe i don't have permissions to send messages there please check my permissions and try again.")

        await asyncio.sleep(realTime)

        my_msg = await textChannel.fetch_message(msg.id)

        try:
            await my_msg.delete()
            await ctx.send(f"The timed message was deleted.")
        except:
            await ctx.send(f"{ctx.author.mention}, I tried to delete the timed message in {textChannel.mention} but i don't have enough permissions to do that, please check my permissions and try again.")

def setup(client):
    client.add_cog(SelfDestruct(client))

import discord
import time
import pytz
import tzlocal
import datetime
from discord.ext import commands

class RamTime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['ramtime2'])
    async def ram_time2(self, ctx):
        dt_utc = datetime.datetime.now(tz = pytz.UTC)
        dt_nzt = dt_utc.astimezone(pytz.timezone("NZ"))
        embed = discord.Embed(title = " :alarm_clock:  Ram Time", color = 0x00FF0C)

        embed.add_field(name = "Time", value = f"{dt_nzt.hour} : {dt_nzt.minute} : {dt_nzt.second}", inline = False)
        embed.add_field(name = "Date", value = f"{dt_nzt.day} / {dt_nzt.month} / {dt_nzt.year}", inline = False)

        await ctx.send(embed = embed)

    @commands.command(aliases = ['ramtime'])
    async def ram_time(self, ctx):
        dt_utc = datetime.datetime.now(tz = pytz.UTC)
        dt_nzt = dt_utc.astimezone(pytz.timezone("NZ"))
        embed = discord.Embed(title = " :alarm_clock:  Ram Time", color = 0x00FF0C)

        embed.add_field(name = "Time", value = f"{dt_nzt.strftime('%I : %M : %S %p')}", inline = False)
        embed.add_field(name = "Date", value = f"{dt_nzt.day} / {dt_nzt.month} / {dt_nzt.year}", inline = False)

        await ctx.send(embed = embed)

    @commands.command(aliases = ['greattime', 'bryantime', 'btime'])
    async def great_time(self, ctx):
        dt_utc = datetime.datetime.now(tz = pytz.UTC)
        dt_nzt = dt_utc.astimezone(pytz.timezone("MST"))
        embed = discord.Embed(title = " :alarm_clock:  Great Time", color = 0xFFA500)

        embed.add_field(name = "Time", value = f"{dt_nzt.strftime('%I : %M : %S %p')}", inline = False)
        embed.add_field(name = "Date", value = f"{dt_nzt.day} / {dt_nzt.month} / {dt_nzt.year}", inline = False)

        await ctx.send(embed = embed)

    @commands.command()
    async def utc(self, ctx):
        utc_time = datetime.datetime.utcnow()
        await ctx.send(f"{utc_time.hour}:{utc_time.minute}:{utc_time.second}")

def setup(client):
    client.add_cog(RamTime(client))

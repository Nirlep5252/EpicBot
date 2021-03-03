import discord
import requests
import os
import json
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import (CommandOnCooldown)

class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client

    def parse_weather_data(self, data):
        data = data['main']
        del data['humidity']
        del data['pressure']
        return data

    def weather_message(self, data, location):
        location = location.title()
        embed = discord.Embed(
            title = f"{location} Weather",
            description = f"Here is the weather data for {location}.",
            color = 0x00FFFF
        )
        embed.add_field(
            name = f"Temperature",
            value = f"{str(data['temp'])}° C",
            inline = False
        )
        embed.add_field(
            name = f"Minimum Temperature",
            value = f"{str(data['temp_min'])}° C",
            inline = False
        )
        embed.add_field(
            name = f"Maximum Temperature",
            value = f"{str(data['temp_max'])}° C",
            inline = False
        )
        embed.add_field(
            name = f"Feels Like",
            value = f"{str(data['feels_like'])}° C",
            inline = False
        )
        return embed

    def error_message(self, location):
        location = location.title()
        return discord.Embed(
            title = f"Error",
            description = f"There was an error finding weather data for {location}.",
            color = 0xFF0000
        )

    @commands.command()
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def weather(self, ctx, *, location = None):
        if location == None:
            await ctx.send("Please enter a location. Usage: `e!weather <location>`")
            return
        API_KEY = os.environ.get("WEATHER_API_KEY")
        URL = f"http://api.openweathermap.org/data/2.5/weather?q={location.lower()}&appid={API_KEY}&units=metric"
        try:
            data = json.loads(requests.get(URL).content)
            data = self.parse_weather_data(data)
            await ctx.send(embed = self.weather_message(data, location))
        except KeyError:
            await ctx.send(embed = self.error_message(location))

def setup(client):
    client.add_cog(Weather(client))

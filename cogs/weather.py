import discord
import requests
import os
import json
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import datetime
from discord.ext.commands import (CommandOnCooldown)

class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client

    #def parse_weather_data(self, data):
        #data = data['main']
        #del data['humidity']
        #del data['pressure']
        #return data

    def weather_message(self, data, location):
        location = location.title()
        embed = discord.Embed(
            title = weather_description,
            #description = f"Here is the weather data for {location}.",
            color = 0x00FFFF
        )
        embed.add_field(
            name = f"Temperature",
            value = f"{str(temp)}° C",
            inline = False
        )
        embed.add_field(
            name = f"Feels Like",
            value = f"{str(feels_like)}° C",
            inline = False
        )
        embed.add_field(
            name = f"Minimum Temperature",
            value = f"{str(min_temp}° C",
            inline = False
        )
        embed.add_field(
            name = f"Maximum Temperature",
            value = f"{str(max_temp)}° C",
            inline = False
        )

        embed.set_thumbnail(
            url= weather_icon_url
        )
        embed.set_author(
            name= f'Weather report of {location}'
        )
        embed.set_footer(
            text=f'Data requested at {datetime.utcnow()}'
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
            data = requests.get(URL)
            #data = self.parse_weather_data(data)
            temp = data.json()['main']['temp']
            feels_like = data.json()['main']['feels_like']
            min_temp = data.json()['main']['temp_min']
            max_temp = data.json()['main']['temp_max']
            weather_icon_url = f'http://openweathermap.org/img/wn/{data.json()['weather'][0]['icon']}.png' 
            weather_description = data.json()['weather'][0]['description']
            
            await ctx.send(embed = self.weather_message(data, location))
        except KeyError:
            await ctx.send(embed = self.error_message(location))

def setup(client):
    client.add_cog(Weather(client))

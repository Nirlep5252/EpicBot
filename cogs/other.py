import discord
import googletrans
import requests
import aiohttp
import datetime
from aiohttp import request
from googletrans import Translator
from discord.ext import commands

numbers = ("1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟")

class Other(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def translate(self, ctx, lang, *, content):
        # t = Translator()
        # a = t.translate(content, dest = lang)
        # await ctx.send(a.text)
        await ctx.send(f"This command is not working temporarily, for more details please join our server - https://discord.gg/Zj7h8Fp")

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def poll(self, ctx, question, *options):
        if len(options) > 10:
            await ctx.send(f"You can only enter upto 10 options. Please try again.")
            return
        else:
            embed = discord.Embed(title = f"**Poll**",
                                description = f"{question}",
                                color = 0x00FF0C)
            embed.add_field(name = f"Options:", value = "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), inline = False)
            embed.add_field(name = "Instructions:", value = f"React with corresponding emotes to vote.", inline = False)
            embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()

            msg = await ctx.send(embed = embed)

            for emoji in numbers[:len(options)]:
                await msg.add_reaction(emoji)

    @commands.command(aliases = ['covid-19', 'covid19'])
    async def covid(self, ctx, *, country = None):
        try:
            if country == None:
                await ctx.send(f"You didn't enter a country name, use the command like this - `e!covid [country]`")
                return
            
            url = f"https://coronavirus-19-api.herokuapp.com/countries/{countryName.lower()}"
            stats = requests.get(url)
            json_stats = stats.json()
            country = json_stats["country"]
            totalCases = json_stats["cases"]
            todayCases = json_stats["todayCases"]
            totalDeaths = json_stats["deaths"]
            todayDeaths = json_stats["todayDeaths"]
            recovered = json_stats["recovered"]
            active = json_stats["active"]
            critical = json_stats["critical"]
            casesPerOneMillion = json_stats["casesPerOneMillion"]
            deathsPerOneMillion = json_stats["deathsPerOneMillion"]
            totalTests = json_stats["totalTests"]
            testsPerOneMillion = json_stats["testsPerOneMillion"]

            embed2 = discord.Embed(title = f"**COVID - 19 Status of {country}**", description = f"This information isn't always live, so it may not be accurate.", color =  0xFFA500)
            embed2.add_field(name = f"Total Cases", value = f"{totalCases}", inline = True)
            embed2.add_field(name = f"Today Cases", value = f"{todayCases}", inline = True)
            embed2.add_field(name = f"Total Deaths", value = f"{totalDeaths}", inline = True)
            embed2.add_field(name = f"Today Deaths", value = f"{todayDeaths}", inline = True)
            embed2.add_field(name = f"Recovered", value = f"{recovered}", inline = True)
            embed2.add_field(name = f"Active", value = f"{active}", inline = True)
            embed2.add_field(name = f"Critical", value = f"{critical}", inline = True)
            embed2.add_field(name = f"Cases Per One Million", value = f"{casesPerOneMillion}", inline = True)
            embed2.add_field(name = f"Deaths Per One Million", value = f"{deathsPerOneMillion}", inline = True)
            embed2.add_field(name = f"Total Tests", value = f"{totalTests}", inline = True)
            embed2.add_field(name = f"Tests Per One Million", value = f"{testsPerOneMillion}", inline = True)
            embed2.set_thumbnail(url = "https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")
            await ctx.send(embed = embed2)
        except:
            await ctx.send("Invalid country name or API error. Please try again.")

    @commands.command()
    async def embed(self, ctx, *, arg=None):
        async def send_error_msg():
            await ctx.send("Invalid args! Correct usage is `e!embed <#hexcolor> | <title> | <description>`")
        
        if arg == None:
            send_error_msg()
            return
        if arg.count(" | ") != 2:
            send_error_msg()
            return
        
        try:
            args = arg.split(" | ")
            col = int(args[0], 16)
        except:
            send_error_msg()
        else:
            title = args[1]
            desc = args[2]
            e = discord.Embed(
                title=title,
                description=desc,
                color=col
            )
            await ctx.send(embed=e)
            
def setup(client):
    client.add_cog(Other(client))

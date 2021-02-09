import discord
import statcord
import requests
import datetime
import os
from discord.ext import commands

class Stats(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.key = os.environ.get("STATCORD_API_KEY")
        self.api = statcord.Client(self.client, self.key)
        self.api.start_loop()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.api.command_run(ctx)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def stats(self, ctx):
        try:
            try:
                url2 = "https://botrix.cc/api/v1/bot/751100444188737617"

                response2 = requests.get(url2)

                votes = response2.json()
                vote_count = votes['bot']['votes']
            except:
                pass

            url = "https://api.statcord.com/v3/751100444188737617"
            response = requests.get(url)
            yes = response.json()

            embed = discord.Embed(title = "Stats",
                                description = "All the stats about bot is shown below.",
                                color = 0x00FFFF)

            embed.add_field(name = "**Servers:**",
                            value = f"{len(self.client.guilds)}",
                            inline = True)
            embed.add_field(name = "**Users:**",
                            value = f"{yes['data'][0]['users']}",
                            inline = True)
            embed.add_field(name = "**Commands ran today:**",
                            value = f"{yes['data'][0]['commands']}",
                            inline = True)
            embed.add_field(name = "**Total cmds:**",
                            value = f"98",
                            inline = True)
            embed.add_field(name = "**Most used cmd:**",
                            value = f"`e!{yes['data'][0]['popular'][0]['name']}` - {yes['data'][0]['popular'][0]['count']} uses",
                            inline = True)
            try:
                embed.add_field(name = "**Total Votes:**",
                                value = f"{vote_count}",
                                inline = True)
            except:
                pass
            embed.add_field(name = "**Ping:**",
                            value = f"{round(self.client.latency * 1000)}ms",
                            inline = True)
            embed.add_field(name = "**Memory Load:**",
                            value = f"{yes['data'][0]['memload']}",
                            inline = True)
            embed.add_field(name = "**CPU Load:**",
                            value = f"{yes['data'][0]['cpuload']}",
                            inline = True)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        except Exception as e:
            print(e)
            await ctx.send(f"An error occured. You are probably being rate limited, Stop spamming the command.")


def setup(client):
    client.add_cog(Stats(client))

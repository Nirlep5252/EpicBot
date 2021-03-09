import discord 
import datetime 
from discord.ext import commands 

class Privacy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def privacy(self, ctx):
        embed = discord.Embed(title = f"EpicBot Privacy Policy",
                                description = "As developers of EpicBot your privacy is our top priority. This Privacy Policy contains types of information that is collected by us along with how we use it.",
                                color = 0x00FFFF)
        embed.add_field(name = "‎", value = "EpicBot and its services use Discord for authentication and in place of having our own accounts, Because of this we store your Discord ID in our secure databases using encryption, While logged in to the website, any account-linked action you perform, such as voting, will be stored with a reference to your Discord ID. Additionally, any data you submit, such as bots or votes, may be stored and displayed on our site via our secure API.\n‎", inline = False)
        embed.add_field(name = "Log Files", value = "We do collect stats for EpicBot so we can improve and see bugs and errors, all logs are stored on a secure Database and all data is kept private.\n‎", inline = False)
        embed.add_field(name = "Who has access to your data?", value = "All user infomation including, Guild ID, User ID and Profiles are used by the bot to Identify you for the Levelling System, and all system data stays on the VPS where no staff or admins have access to it.\n‎", inline = False)
        embed.add_field(name = "Stats data", value = "We do log stats for our bot which are publicy available this includes, Commands run, Active users. No user data can be accessed by staff or admins.", inline = False)

        embed.add_field(name = "‎",
                        value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                        inline = False)
        embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
        embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Privacy(client))
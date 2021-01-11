import discord
import datetime
import os
from discord.ext import commands
from pymongo import MongoClient

conn = MongoClient(os.environ.get("MONGODB_LINK"))
db = conn["EpicBot"]

welcome = db["real_welcome"]
leave = db["real_leave"]

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):

        mention = member.mention
        guild = member.guild

        channel_logging = self.client.get_channel(762597664679788575)

        # print(f'{member} has joined {guild.name}.')
        # await channel_logging.send(f"`{member} ({member.id})` just joined `{guild.name} ({guild.id})`.")

        if guild.id == 746202728031584358: # - EPICPALACE
            await member.create_dm()
            await member.dm_channel.send(str(f"Hey {mention}!, Welcome to {guild}! Make sure you read the rules! Hope you have fun and have a nice day!").format(mention=mention, guild=guild))

            embed = discord.Embed(title=str("***New Member Joined***"), color=0x00FF0C, description=str(f"{mention} joined {guild} :tada: :sparkles:").format(mention=mention, guild=guild))
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name="User ID: ", value=member.id)
            embed.add_field(name="User Name: ", value=member.display_name)
            embed.add_field(name="Server Name: ", value=guild)
            embed.add_field(name="Total Members: ", value=len(list(guild.members)))
            embed.add_field(name="Creation Date: ", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.add_field(name="Join Date: ", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.set_image(url = "https://cdn.discordapp.com/attachments/749996055369875459/773509331370246174/welcome.gif")

            channel = discord.utils.get(member.guild.channels, id=int("746202728375648270"))
            await channel.send(embed=embed)

        elif guild.id == 719157704467152977: # RAMS SERVER
            await member.create_dm()
            await member.dm_channel.send(str(f"Hey {mention}!, Welcome to {guild}! Make sure you read the rules! Hope you have fun and have a nice day!").format(mention=mention, guild=guild))

            embed = discord.Embed(title=str("***New Member Joined***"), color=0x00FF0C, description=str(f"{mention} joined {guild} :tada: :sparkles:").format(mention=mention, guild=guild))
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name="User ID: ", value=member.id)
            embed.add_field(name="User Name: ", value=member.display_name)
            embed.add_field(name="Server Name: ", value=guild)
            embed.add_field(name="Total Members: ", value=len(list(guild.members)))
            embed.add_field(name="Creation Date: ", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.add_field(name="Join Date: ", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.set_image(url = "https://cdn.discordapp.com/attachments/749996055369875459/773509331370246174/welcome.gif")

            channel = discord.utils.get(member.guild.channels, id=int("719168017514102916"))
            await channel.send(embed=embed)

        elif guild.id == 718234216382333021: # BRYANS SERVER
            await member.create_dm()
            await member.dm_channel.send(str(f"Hey {mention}!, Welcome to {guild}! Make sure you read the rules! Hope you have fun and have a nice day!").format(mention=mention, guild=guild))

            embed = discord.Embed(title=str("***New Member Joined***"), color=0x00FF0C, description=str(f"{mention} joined {guild} :tada: :sparkles:").format(mention=mention, guild=guild))
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name="User ID: ", value=member.id)
            embed.add_field(name="User Name: ", value=member.display_name)
            embed.add_field(name="Server Name: ", value=guild)
            embed.add_field(name="Total Members: ", value=len(list(guild.members)))
            embed.add_field(name="Creation Date: ", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.add_field(name="Join Date: ", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.set_image(url = "https://cdn.discordapp.com/attachments/749996055369875459/773509331370246174/welcome.gif")

            channel = discord.utils.get(member.guild.channels, id=int("718234216852357150"))
            await channel.send(embed=embed)

        elif guild.id == 778954023213596683:
            await member.create_dm()
            await member.dm_channel.send(str(f"Hey {mention}!, Welcome to {guild}! Make sure you read the rules! Hope you have fun and have a nice day!").format(mention=mention, guild=guild))

            embed = discord.Embed(title=str("***New Member Joined***"), color=0x00FF0C, description=str(f"{mention} joined {guild} :tada: :sparkles:").format(mention=mention, guild=guild))
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name="User ID: ", value=member.id)
            embed.add_field(name="User Name: ", value=member.display_name)
            embed.add_field(name="Server Name: ", value=guild)
            embed.add_field(name="Total Members: ", value=len(list(guild.members)))
            embed.add_field(name="Creation Date: ", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.add_field(name="Join Date: ", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.set_image(url = "https://cdn.discordapp.com/attachments/749996055369875459/773509331370246174/welcome.gif")

            channel = discord.utils.get(member.guild.channels, id=int("778961935487598602"))
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        mention = member.mention
        guild = member.guild

        channel_logging = self.client.get_channel(762597664679788575)

        # print(f'{member} has left {guild.name}.')
        # await channel_logging.send(f"`{member}` just left `{guild.name}`.")


        if guild.id == 746202728031584358:
            embed = discord.Embed(title=str("***Member Left***"), color=0xFF0000, description=str(f"{mention} left {guild} :disappointed_relieved: :sob:").format(mention=mention, guild=guild))
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name="User ID: ", value=member.id)
            embed.add_field(name="User Name: ", value=member.display_name)
            embed.add_field(name="Server Name: ", value=guild)
            embed.add_field(name="Total Members: ", value=len(list(guild.members)))

            channel = discord.utils.get(member.guild.channels, id=int("749223249715658753"))
            await channel.send(embed=embed)
        elif guild.id == 719157704467152977:
            embed = discord.Embed(title=str("***Member Left***"), color=0xFF0000, description=str(f"{mention} left {guild} :disappointed_relieved: :sob:").format(mention=mention, guild=guild))
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
            embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            embed.add_field(name="User ID: ", value=member.id)
            embed.add_field(name="User Name: ", value=member.display_name)
            embed.add_field(name="Server Name: ", value=guild)
            embed.add_field(name="Total Members: ", value=len(list(guild.members)))

            channel = discord.utils.get(member.guild.channels, id=int("719168017514102916"))
            await channel.send(embed=embed)

def setup(client):
    client.add_cog(Welcome(client))

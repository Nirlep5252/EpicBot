import discord 
import asyncio
import random 
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import (CommandOnCooldown)
from discord.ext import commands 

class HACK(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command()
    async def hack(self, ctx, user: discord.Member = None):
        if user == None:
            await ctx.send("Please tell me who do you want to hack.")

        elif user == ctx.author:
            await ctx.send("You shouldn't hack yourself.")

        else:
            email_fun = ['69420', '8008135', 'eatsA$$', 'PeekABoo',
                            'TheShire', 'isFAT', 'Dumb_man', 'Ruthless_gamer',
                            'Sexygirl69', 'Loyalboy69', 'likesButts']

            email_address = f"{user.name.lower()}{random.choice(email_fun).lower()}@gmail.com"
                            
            passwords = ['animeislife69420', 'big_awoogas', 'red_sus_ngl',
                            'IamACompleteIdiot', 'YouWontGuessThisOne',
                            'yetanotherpassword', 'iamnottellingyoumypw',
                            'SayHelloToMyLittleFriend', 'ImUnderYourBed',
                            'TellMyWifeILoveHer', 'P@$$w0rd', 'iLike8008135', 'IKnewYouWouldHackIntoMyAccount',
                            'BestPasswordEver', 'JustARandomPassword']
                            
            password = f"{random.choice(passwords)}"

            DMs = ["send nudes please", "i invited epicbot and i got a cookie",
                    "i hope my mum doesn't find my nudes folder",
                    "please dont bully me", "https://youtu.be/oHg5SJYRHA0", 
                    "i like bananas", "black jellybeans are the best jellybeans",
                    "i use discord in light mode"]

            latest_DM = f"{random.choice(DMs)}"

            ip_address = f"690.4.2.0:{random.randint(1000, 9999)}"

            Discord_Servers = ["Sons of Virgins", "Small Benis Gang", "Gamers United",
                                    "Anime_Server_69420", "CyberDelayed 2077", "I love Corn"]

            Most_Used_Discord_Server = f"{random.choice(Discord_Servers)}"


            msg1 = await ctx.send("Initializing Hack.exe... <a:EpicLoading1:762919634336088074>")
            await asyncio.sleep(1)

            real_msg1 = await ctx.channel.fetch_message(msg1.id)
            await real_msg1.edit(content = f"Successfully initialized Hack.exe, beginning hack on {user.name}... <a:EpicLoading1:762919634336088074>")
            await asyncio.sleep(1)

            real_msg2 = await ctx.channel.fetch_message(msg1.id)
            await real_msg2.edit(content = f"Logging into {user.name}'s Discord Account... <a:EpicLoading1:762919634336088074>")
            await asyncio.sleep(1)

            real_msg3 = await ctx.channel.fetch_message(msg1.id)
            await real_msg3.edit(content = f"<:EpicDiscord:770889292746194964> Logged into {user.name}'s Discord:\nEmail Address: `{email_address}`\nPassword: `{password}`")
            await asyncio.sleep(1)

            real_msg4 = await ctx.channel.fetch_message(msg1.id)
            await real_msg4.edit(content = f"Fetching DMs from their friends(if there are any)... <a:EpicLoading1:762919634336088074>")
            await asyncio.sleep(1)

            real_msg5 = await ctx.channel.fetch_message(msg1.id)
            await real_msg5.edit(content = f"Latest DM from {user.name}: `{latest_DM}`")
            await asyncio.sleep(1)

            real_msg6 = await ctx.channel.fetch_message(msg1.id)
            await real_msg6.edit(content = f"Getting IP address... <a:EpicLoading1:762919634336088074>")
            await asyncio.sleep(1)

            real_msg7 = await ctx.channel.fetch_message(msg1.id)
            await real_msg7.edit(content = f"IP address found: `{ip_address}`")
            await asyncio.sleep(1)

            real_msg11 = await ctx.channel.fetch_message(msg1.id)
            await real_msg11.edit(content = f"Fetching the Most Used Discord Server... <a:EpicLoading1:762919634336088074>")
            await asyncio.sleep(1)

            real_msg10 = await ctx.channel.fetch_message(msg1.id)
            await real_msg10.edit(content = f"Most used Discord Server in {user.name}'s Account: `{Most_Used_Discord_Server}`")
            await asyncio.sleep(1)

            real_msg8 = await ctx.channel.fetch_message(msg1.id)
            await real_msg8.edit(content = f"Selling data to the dark web... <a:EpicLoading1:762919634336088074>")
            await asyncio.sleep(1)

            real_msg9 = await ctx.channel.fetch_message(msg1.id)
            await real_msg9.edit(content = f"Hacking complete.")
            await ctx.send(f"{user.name} has successfully been hacked. <a:EpicTik:766172079179169813>\n\n**{user.name}**'s Data:\nDiscord Email: `{email_address}`\nDiscord Password: `{password}`\nMost used Discord Server: `{Most_Used_Discord_Server}`\nIP Address: `{ip_address}`\nLatest DM: `{latest_DM}`")


def setup(client):
    client.add_cog(HACK(client))
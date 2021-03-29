import discord
import datetime
import random
import aiohttp
import requests
import pyfiglet
import os
import asyncio 
from discord.ext import commands
from config import *

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def chat(self, ctx, *, msg: str = None):
        if msg == None:
            await ctx.message.reply("Hello! In order to chat with me use: `e!chat <message>`")
            return

        response = requests.get(f"https://rdch.dev64.repl.co/chat?message={msg}").json()['reply']

        await ctx.message.reply(response)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def whendie(self, ctx, *, user: discord.Member = None):
        if user == None:
            user = ctx.author

        msg = await ctx.message.reply(embed=discord.Embed(title="Let's see when you're gonna die...", color=MAIN_COLOR))

        something = [
            f'{random.randint(0, 60)} Second(s)',
            f'{random.randint(1, 60)} Minute(s)',
            f'{random.randint(1, 24)} Hour(s)',
            f'{random.randint(1, 7)} Day(s)',
            f'{random.randint(1, 4)} Week(s)',
            f'{random.randint(1, 100)} Year(s)'
        ]

        thingy = random.choice(something)

        if thingy == something[0]:
            funny_text = "LOL YOU'RE DEAD"
            embed_color = RED_COLOR
        if thingy == something[1]:
            funny_text = "Well rip, you're almost dead"
            embed_color = RED_COLOR
        if thingy == something[2]:
            funny_text = "Sad"
            embed_color = RED_COLOR
        if thingy == something[3]:
            funny_text = "Ok you have some time before you die"
            embed_color = ORANGE_COLOR
        if thingy == something[4]:
            funny_text = "You're not dying that early, Yay!"
            embed_color = ORANGE_COLOR
        if thingy == something[5]:
            funny_text = "Wowie, you have a nice long life! OwO"
            embed_color = MAIN_COLOR

        embed = discord.Embed(
            description = f"{user.mention} is gonna die in **{thingy}**",
            color = embed_color,
        )
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.set_footer(text=funny_text)

        await msg.edit(embed=embed)
        
    @commands.command()
    async def owo(self, ctx, *, msg):

        vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']

        def last_replace(s, old, new):
            li = s.rsplit(old, 1)
            return new.join(li)

        def text_to_owo(text):
            """ Converts your text to OwO """
            smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)']

            text = text.replace('L', 'W').replace('l', 'w')
            text = text.replace('R', 'W').replace('r', 'w')

            text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
            text = last_replace(text, '?', '? owo')
            text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))

            for v in vowels:
                if 'n{}'.format(v) in text:
                    text = text.replace('n{}'.format(v), 'ny{}'.format(v))
                if 'N{}'.format(v) in text:
                    text = text.replace('N{}'.format(v), 'N{}{}'.format('Y' if v.isupper() else 'y', v))

            return text

        await ctx.send(text_to_owo(msg))             

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['bait', 'freenitro', 'nitrobait', 'keknitro'])
    async def jebait(self, ctx):
        embed = discord.Embed(title = "FREE NITRO", description = f"[https://discord.gift/NBnj8bySBWr63Q99](https://discord.gg/Zj7h8Fp)", color = 0x00FFFF)

        try:
            await ctx.message.delete()
        except:
            pass

        await ctx.send(embed = embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['randomname'])
    async def random_name(self, ctx):
        await ctx.message.reply(requests.get("https://nekos.life/api/v2/name").json()['name'])

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Shows how cute you are, I know you are a cutie!")
    async def howcute(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        embed = discord.Embed(
            title = "Calculating cuteness...",
            color = MAIN_COLOR
        )
        msg1 = await ctx.message.reply(embed=embed)

        cute_number = random.randint(0, 100)

        if 0 <= cute_number <= 20:
            lol = "Damn, you're ugly!"
            embed_color_uwu = RED_COLOR
        if 20 < cute_number <= 50:
            lol = "Not bad!"
            embed_color_uwu = ORANGE_COLOR
        if 50 < cute_number <= 75:
            lol = "You're kinda cute, UwU"
            embed_color_uwu = MAIN_COLOR
        if 75 < cute_number <= 100:
            lol = "Holy fuck, you're cute! ><"
            embed_color_uwu = MAIN_COLOR

        embed = discord.Embed(
            title="Cuteness detector!",
            description = f"**{user.name}#{user.discriminator}** is **{cute_number}%** cute!",
            color = embed_color_uwu
        )
        embed.set_footer(text=lol)

        await msg1.edit(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def howhorny(self, ctx, *, user: discord.Member = None):
        if user == None:
            user = ctx.author
        embed = discord.Embed(
            title = "Calculating how horny you are...",
            color = MAIN_COLOR
        )
        msg = await ctx.message.reply(embed=embed)

        percentage = random.randint(0, 100)

        if 0 <= percentage <= 20:
            lol = "You are a happy person."
            embed_color_uwu = MAIN_COLOR
        if 20 < percentage <= 50:
            lol = "Hmm"
            embed_color_uwu = ORANGE_COLOR
        if 50 < percentage <= 75:
            lol = "You're kinda horny, OwO"
            embed_color_uwu = MAIN_COLOR
        if 75 < percentage <= 100:
            lol = "You are very horny!"
            embed_color_uwu = PINK_COLOR

        await msg.edit(
            embed = discord.Embed(
                title = "Hornyness detector!",
                description = f"**{user.name}#{user.discriminator}** is **{percentage}%** horny!",
                color = embed_color_uwu
            ).set_footer(text=lol)
        )

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Calculates how gay the user is!")
    async def howgay(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        embed = discord.Embed(
            title="Calculating how gay you are...",
            color=MAIN_COLOR
        )
        msg = await ctx.message.reply(embed=embed)

        cute_number = random.randint(0, 100)

        if 0 <= cute_number <= 20:
            embed_color_uwu = RED_COLOR
        if 20 < cute_number <= 50:
            embed_color_uwu = ORANGE_COLOR
        if 50 < cute_number <= 100:
            embed_color_uwu = MAIN_COLOR

        embed = discord.Embed(
            title="Gayness Detector!",
            description=f"**{user.name}#{user.discriminator}** is **{cute_number}%** gay!",
            color=embed_color_uwu
        )

        await msg.edit(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['simpfor'])
    async def simp_for(self, ctx, user: discord.Member = None):
        if user == None:
            await ctx.send(f"Please enter a user you want simp for.")
            return

        embed = discord.Embed(title = "New Simp", description = f"{ctx.author.mention} just simped for {user.mention} <a:EpicPeepoSimp:758955006039818261>.", color = 0xFFC0CB)
        embed.set_thumbnail(url = user.avatar_url)
        await ctx.message.reply(embed = embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['dadjoke', 'joke', 'ramjoke', 'ram_joke'])
    async def dad_joke(self, ctx):
        url = "https://joke3.p.rapidapi.com/v1/joke"

        headers = {
            'x-rapidapi-host': "joke3.p.rapidapi.com",
            'x-rapidapi-key': os.environ.get("RAPID_API_KEY")
            }

        response = requests.request("GET", url, headers=headers)
        joke = response.json()

        await ctx.message.reply(joke['content'])

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def quote(self, ctx):
        results = requests.get('https://type.fit/api/quotes').json()
        num = random.randint(1, 1500)
        content = results[num]['text']
        await ctx.message.reply(content)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def say(self, ctx, *, msg = None):
        filter = ['@here', '@everyone', '<@&', '<@!']

        for word in filter:
            if msg.count(word) > 0:
                await ctx.message.reply(f"Sorry, I won't ping anyone. Try something else.")
                return

        if msg == None:
            await ctx.message.reply(f"Please enter a message that you want me to say.")
        else:
            await ctx.message.reply(msg)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def advice(self, ctx):
        url = "https://api.adviceslip.com/advice"
        response = requests.get(url)
        advice = response.json()
        real_advice = advice['slip']['advice']
        await ctx.message.reply(real_advice)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def ascii(self, ctx, *, text = None):
        if text == None:
            await ctx.message.reply(f"Please enter some text.")
        else:
            if len(pyfiglet.figlet_format(text)) > 2000:
                await ctx.message.reply(f"Text too long. Please enter short text.")
            else:
                await ctx.message.reply(f"```{pyfiglet.figlet_format(text)}```")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def mock(self, ctx, *,text=None):

        if text == None:
            await ctx.message.reply("Please enter some text!")
        else:

            filter = ['@here', '@everyone', '<@&', '<@!']

            for word in filter:
                if text.count(word) > 0:
                    await ctx.message.reply(f"Sorry, I won't ping anyone. Try something else.")
                    return

            res = ""
            for c in text:
                chance = random.randint(0,1)
                if chance:
                    res += c.upper()
                else:
                    res += c.lower()
            await ctx.message.reply(res)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=["atc"])
    async def aesthetic(self, ctx, *, args=None):
        if args == None:
            await ctx.send("Invalid args. Correct usage: `e!atc <msg> | [mode]`. Mode can be b (bold), i (italic), or n (none).")
            return

        if args.count(" | ") == 0:
            m = "n"
        else:
            m = args[-1]

        s = ""
        if m == "b":
            s += "**"
        elif m == "i":
            s += "_"

        msg = "".join(args.split(" | ")[0])
        args = args.split(" | ")[:-1]
        for c in msg:
            s += c + " "
        if m == "b":
            s += "**"
        elif m == "i":
            s += "_"

        await ctx.message.reply(s)

    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.command()
    async def hack(self, ctx, user: discord.Member = None):
        if user == None:
            await ctx.message.reply(embed=discord.Embed(
                title = "Error!",
                description = "You didn't mention who to hack. Please try again!",
                color = RED_COLOR
            ))

        elif user == ctx.author:
            await ctx.message.reply("You shouldn't hack yourself.")

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
    client.add_cog(Fun(client))

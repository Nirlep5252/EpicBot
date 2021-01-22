import discord
import datetime
import random
import aiohttp
import requests
import pyfiglet
import os
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['bait', 'freenitro', 'nitrobait', 'keknitro'])
    async def jebait(self, ctx):
        embed = discord.Embed(title = "FREE NITRO", description = f"[https://discord.gift/NBnj8bySBWr63Q99](https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstleyVEVO)", color = 0x00FFFF)

        try:
            await ctx.message.delete()
        except:
            pass

        await ctx.send(embed = embed)

    @commands.command(aliases = ['howcute'])
    async def how_cute(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author

        randomFaces = ['uwu','owo', ';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)', '>.<']

        embed = discord.Embed(title = "Cuteness Detector", description = f"{user.mention} is **{random.randint(0, 100)}%** cute. {random.choice(randomFaces)}", color = 0xFFC0CB)
        embed.set_thumbnail(url = user.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['simpfor'])
    async def simp_for(self, ctx, user: discord.Member = None):
        if user == None:
            await ctx.send(f"Please enter a user you want simp for.")
            return

        embed = discord.Embed(title = "New Simp", description = f"{ctx.author.mention} just simped for {user.mention} <a:EpicPeepoSimp:758955006039818261>.", color = 0xFFC0CB)
        embed.set_thumbnail(url = user.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['dadjoke', 'joke', 'ramjoke', 'ram_joke'])
    async def dad_joke(self, ctx):
        url = "https://joke3.p.rapidapi.com/v1/joke"

        headers = {
            'x-rapidapi-host': "joke3.p.rapidapi.com",
            'x-rapidapi-key': os.environ.get("RAPID_API_KEY")
            }

        response = requests.request("GET", url, headers=headers)
        joke = response.json()

        await ctx.send(joke['content'])

    @commands.command()
    async def quote(self, ctx):
        results = requests.get('https://type.fit/api/quotes').json()
        num = random.randint(1, 1500)
        content = results[num]['text']
        await ctx.send(content)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command()
    async def hug(self, ctx, user: discord.Member):
        hugs = ['https://acegif.com/wp-content/gif/anime-hug-86.gif',
                'https://acegif.com/wp-content/gif/anime-hug-19.gif',
                'https://i.pinimg.com/originals/f2/80/5f/f2805f274471676c96aff2bc9fbedd70.gif',
                'https://acegif.com/wp-content/uploads/anime-hug.gif',
                'https://i.pinimg.com/originals/85/72/a1/8572a1d1ebaa45fae290e6760b59caac.gif',
                'https://64.media.tumblr.com/296601d3c45ceea663f5d5dd052025c3/dad1de4967f02b18-56/s640x960/e77460ffb4d1900c59131faf08c448efe41f1d3e.gif']

        embed = discord.Embed(title = "Incoming Hug... ", description = f"{ctx.author.mention} just gave a strong hug to {user.mention} <a:EpicHug:766549597493395457>", color = 0x00FF0C)
        embed.set_image(url = random.choice(hugs))
        embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)

    @commands.command()
    async def say(self, ctx, *, msg = None):
        filter = ['@here', '@everyone', '<@&', '<@!']

        for word in filter:
            if msg.count(word) > 0:
                await ctx.send(f"Sorry, I won't ping anyone. Try something else.")
                return

        if msg == None:
            await ctx.send(f"Please enter a message that you want me to say.")
        else:
            await ctx.send(msg)
        # await ctx.send("This command is temporarily unavailable. Join our discord server -> discord.gg/Zj7h8Fp")

    @commands.command(aliases=['meow', 'simba', 'cats'])
    async def cat(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r:
                    data = await r.json()

                    embed = discord.Embed(title = "Meow! <:EpicConfusedCat:750217867898650644>", color = 0x00FF0C)
                    embed.set_image(url = data['file'])

                    await ctx.send(embed=embed)

    @commands.command(aliases=['dogs'])
    async def dog(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://random.dog/woof.json") as r:
                    data = await r.json()

                    embed = discord.Embed(title = "Woof!", color = 0x00FF0C)
                    embed.set_image(url = data['url'])

                    await ctx.send(embed=embed)

    @commands.command()
    async def advice(self, ctx):
        url = "https://api.adviceslip.com/advice"
        response = requests.get(url)
        advice = response.json()
        real_advice = advice['slip']['advice']
        await ctx.send(real_advice)

    @commands.command()
    async def ascii(self, ctx, *, text = None):
        if text == None:
            await ctx.send(f"Please enter some text.")
        else:
            if len(pyfiglet.figlet_format(text)) > 2000:
                await ctx.send(f"Text too long. Please enter short text.")
            else:
                await ctx.send(f"```{pyfiglet.figlet_format(text)}```")


    @commands.command()
    async def fox(self, ctx):
        url = "https://randomfox.ca/floof/"
        response = requests.get(url)
        fox = response.json()

        embed = discord.Embed(color = 0x00FFFF)
        embed.set_image(url = fox['image'])
        await ctx.send(embed = embed)

    @commands.command()
    async def lurk(self, ctx):
        if ctx.guild.id != 719157704467152977:
            await ctx.send(f"This is private command you can't use it here.")
            return
        user = ctx.author
        await ctx.send(f"{user.mention} has gone to get Chicken Nuggets! We will miss them! ok bye:tm:")
   
    @commands.command()
    async def mock(self, ctx, *,text=None):
        if text == None:
            await ctx.send("Please enter some text!")
        else:
            res = ""
            for c in text:
                chance = random.randint(0,1)
                if chance:
                    res += c.upper()
                else:
                    res += c.lower()
            await ctx.send(res)
            
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
        
        m = "".join(args.split(" | "))
        for c in m:
            s += c + " "
        if m == "b":
            s += "**"
        elif m == "i":
            s += "_"
        
        await ctx.send(s)
        

def setup(client):
    client.add_cog(Fun(client))

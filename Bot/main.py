import discord
import json
import os
import random
import datetime
import typing as t
import asyncio
import aiohttp
import requests
import time
from typing import Optional
from aiohttp import request
from discord import Member, Embed
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import (CommandOnCooldown)
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from discord import DMChannel
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

numbers = ("1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟")


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(
    command_prefix = commands.when_mentioned_or("e!", "E!"),
    intents = intents,
    case_insensitive = True
)
client.remove_command('help')

mainshop = [{"name":"Laptop","price":25000,"description":"For Working."},
            {"name":"PC","price":100000,"description":"Gaming and Streaming."},
            {"name":"Phone","price":10000,"description":"In order to call someone."},
            {"name":"FLEX","price":1000000,"description":"In order to flex on other people."}]

players = {}

@tasks.loop(seconds=30)
async def change_status():
    await client.change_presence(activity=discord.Game(name = f"e!help | {len(client.guilds)} Servers!"))

@client.event
async def on_ready():
    print("Bot is now online!")
    change_status.start()

start = time.time()

@client.command()
async def uptime(ctx):
    uptime = round((time.time() - start)/60, 2)
    uptime_day = round((time.time() - start)/216000, 2)
    uptime_hour = round((time.time() - start)/3600, 2)
    uptime_min = round((time.time() - start)/60, 2)
    uptime_sec = round((time.time() - start), 2)

    if uptime < 1:
        await ctx.send(f"{uptime_sec} seconds.")

    elif uptime > 1 and uptime < 60:
        await ctx.send(f"{uptime_min} minutes.")

    elif uptime > 60 and uptime_day < 1:
        await ctx.send(f"{uptime_hour} hours.")

    elif uptime_day > 1:
        await ctx.send(f"{uptime_day} days.")

@client.command(aliases = ['memberinfo', 'user_info', 'member_info'])
async def userinfo(ctx, target: Optional[Member]):
    target = target or ctx.author

    embed = discord.Embed(title = "__**User Information**__", color = 0x00FFFF)
    embed.set_thumbnail(url = target.avatar_url)
    embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
    embed.timestamp = datetime.datetime.utcnow()

    fields = [("ID", f"`{target.id}`", False),
                ("Username", f"`{str(target)}`", True),
                ("Top Roles", target.top_role.mention, True),
                ("Server Boosts", bool(target.premium_since), False),
                ("Created At", target.created_at.strftime("%d/%m/%y | %H:%M:%S"), False),
                ("Joined At", target.joined_at.strftime("%d/%m/%y | %H:%M:%S"), False)]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    await ctx.send(embed=embed)

@client.command()
async def wanted(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    wanted = Image.open("images/wanted.jpg")

    asset = user.avatar_url_as(size = 4096, format="png")
    data = BytesIO(await asset.read())
    profile_pic = Image.open(data)

    profile_pic = profile_pic.resize((340, 340))
    wanted.paste(profile_pic, (80, 181))

    wanted.save("epic_wanted.jpg")

    await ctx.send(file = discord.File("epic_wanted.jpg"))

@client.command(aliases = ['mental', 'illness', 'mentalillness', 'illness_mental', 'illnessmental'])
async def mental_illness(ctx, *, text = "I didn't use to put any text in the mental illness command."):

    img = Image.open("images/illness.jpg")

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 33)

    draw.text((115, 926), text, (255, 255, 255), font = font)
    img.save("epic_illness.jpg")
    await ctx.send(file = discord.File("epic_illness.jpg"))

@client.command(aliases = ['fax', 'facts'])
async def fact(ctx, *, text = "You didn't put any text here."):
    img = Image.open("images/facts.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 25)
    draw.text((55, 700), text, (0, 0, 0), font = font)
    img.save("epic_facts.jpg")
    await ctx.send(file = discord.File("epic_facts.jpg"))

@client.command(aliases = ['shocked', 'ramshocked', 'ram_shocked'])
async def shock(ctx, *, text = "You have to put some text here."):

    img = Image.open("images/ram_shocked.jpg")

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 35)

    draw.text((7, 5), text, (0, 0, 0), font = font)
    img.save("epic_shocked.jpg")
    await ctx.send(file = discord.File("epic_shocked.jpg"))

@client.command(aliases = ['trump', 'trumpsays', 'trumpsaid', 'trump_said'])
async def trump_says(ctx, *, text = f"You didn't enter\nany text here."):

    img = Image.open("images/trump.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 38)
    draw.text((360, 286), text, (0, 0, 0), font = font)
    img.save("epic_trump.jpg")
    await ctx.send(file = discord.File("epic_trump.jpg"))

@client.command()
async def burn(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    burn = Image.open("images/burn.jpg")

    asset = user.avatar_url_as(size = 4096, format="png")
    data = BytesIO(await asset.read())
    profile_pic = Image.open(data)

    profile_pic = profile_pic.resize((342, 342))
    burn.paste(profile_pic, (117, 217))

    burn.save("epic_burn.jpg")

    await ctx.send(file = discord.File("epic_burn.jpg"))

@client.command()
async def angry(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    angry = Image.open("images/angry.jpg")

    asset = user.avatar_url_as(size = 4096, format="png")
    data = BytesIO(await asset.read())
    profile_pic = Image.open(data)

    profile_pic = profile_pic.resize((91, 91))
    angry.paste(profile_pic, (426, 483))

    angry.save("epic_angry.jpg")

    await ctx.send(file = discord.File("epic_angry.jpg"))

@client.command()
async def trash(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author

    trash = Image.open("images/trash.jpg")

    asset = user.avatar_url_as(size = 4096, format="png")
    data = BytesIO(await asset.read())
    profile_pic = Image.open(data)

    profile_pic = profile_pic.resize((179, 179))
    trash.paste(profile_pic, (374, 66))

    trash.save("epic_trash.jpg")

    await ctx.send(file = discord.File("epic_trash.jpg"))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename[:-3]}')

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"Loaded {extension}")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f"Unloaded {extension}")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"Reloaded {extension}")

@load.error
async def load_error(ctx, error):
    print(error)

@unload.error
async def unload_error(ctx, error):
    print(error)

@reload.error
async def reload_error(ctx, error):
    print(error)

@client.event
async def on_message(message):
    channel = message.channel
    channel_logging = client.get_channel(762597664679788575)
    dm_logging = client.get_channel(793482521076695070)
    user = message.author
    guild = message.guild

    await client.process_commands(message)

    if message.author == client.user:
        return

@client.command(aliases=['createinvite'])
@commands.has_permissions(create_instant_invite = True)
async def create_invite(ctx):
    link = await ctx.channel.create_invite(max_age=0)
    await ctx.send(link)

# Economy Starts here.------------------------------------
@commands.cooldown(1, 10, commands.BucketType.user)
@client.command(aliases = ['bal'])
async def balance(ctx):
    await open_account(ctx.author)

    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title = f"**{ctx.author.name}'s balance**", color = 0x00FF0C)
    em.add_field(name = "Wallet", value = f":coin:  {wallet_amt} EpicCoins", inline = False)
    em.add_field(name = "Bank", value = f":coin:  {bank_amt} EpicCoins", inline = False)
    em.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
    em.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed = em)

@commands.cooldown(1, 30, commands.BucketType.user)
@client.command()
async def beg(ctx):

    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    earnings = random.randrange(101)

    await ctx.send(f"Nirlep just gave you :coin: {earnings} EpicCoins! <:EpicPogU:750213927484260493>")

    users[str(user.id)]["wallet"] += earnings

    with open("moneybank.json", "w") as f:
        json.dump(users, f)

# Error Handling -------
@client.event
async def on_command_error(ctx, error):
    embed = discord.Embed(
        title='',
        color=discord.Color.red())
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is on cooldown, please try again after **{:.2f}** seconds.'.format(error.retry_after)
        await ctx.message.reply(msg)
        return

    if isinstance(error, commands.MissingPermissions):
        await ctx.message.reply(f"You don't have sufficient permissions to execute this command.")
        return

    if isinstance(error, commands.BotMissingPermissions):
        await ctx.message.reply(f"Looks like I don't have enough permissions to do that please try again after checking my permissions.")
        return

    if isinstance(error, commands.errors.MemberNotFound):
        await ctx.message.reply(f"I wasn't able to find that user please try again.")
        return

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.reply(f"Please enter all the required arguments for the command. Type `e!help` for more info on the commands.")
        return

    if isinstance(error, commands.BadArgument):
        await ctx.message.reply(f"One or more of the arguments is invalid please try again.")
        return

    if isinstance(error, commands.NotOwner):
        await ctx.message.reply(f"i see a cocksucker trying to use owner only commands")
        return
    else:
        embed.add_field(name=f':x: Terminal Error', value=f"```{error}```")
        await client.get_channel(800252938869669898).send(embed=embed)
        raise error

# Economy continues ------------------
@client.command(aliases = ['with'])
async def withdraw(ctx, amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter some amount.")
        return

    bal = await update_bank(ctx.author)

    if amount == "all":
        amount = bal[1]

    if amount == "max":
        amount = bal[1]

    amount = int(amount)
    if amount>bal[1]:
        await ctx.send("You don't have that much money in your bank.")
        return
    if amount<0:
        await ctx.send("You can't withdraw negative money.")
        return

    await update_bank(ctx.author,amount,"wallet")
    await update_bank(ctx.author,-1*amount,"bank")

    await ctx.send(f"Congrats! You successfully withdrew :coin: {amount} EpicCoins!")

@client.command(aliases=['dep'])
async def deposit(ctx, amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter some amount.")
        return

    bal = await update_bank(ctx.author)

    if amount == "all":
        amount = bal[0]

    if amount == "max":
        amount = bal[0]

    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("You don't have that much money in your wallet.")
        return
    if amount<0:
        await ctx.send("You can't deposit negative money.")
        return

    await update_bank(ctx.author,-1*amount,"wallet")
    await update_bank(ctx.author,amount,"bank")

    await ctx.send(f"Congrats! You successfully deposited :coin: {amount} EpicCoins!")

@commands.cooldown(1, 30, commands.BucketType.user)
@client.command()
async def slots(ctx, amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter some amount.")
        return

    bal = await update_bank(ctx.author)

    if amount == "all":
        amount = bal[0]

    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("You don't have enough money in your wallet.")
        return
    if amount<0:
        await ctx.send("You can't own negative money.")
        return

    final = []
    for i in range(3):
        a = random.choice(["💗","🏆","👑"])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] == final[2]:
        await update_bank(ctx.author, 5*amount)
        await ctx.send("GG! Bro, you won!")
    else:
        await update_bank(ctx.author, -1*amount)
        await ctx.send("You lost!")

@client.command()
async def shop(ctx):
    em = discord.Embed(title = "**Shop**",description = "Down below is the list of all the items in the shop. type `e!buy [item]` to buy any of these items.", color = 0x00FF0C)


    for item in mainshop:
        name = item["name"]
        price = item["price"]
        description = item["description"]
        em.add_field(name = f"{name} - __:coin: {price}__", value = f"{description}", inline=False)
        em.set_thumbnail(url='https://media.discordapp.net/attachments/749996055369875459/751648770185494548/EP2.png')

    await ctx.send(embed = em)

@client.command()
async def buy(ctx, item, amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author, item, amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That item doesn't exist in the shop.")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet.")
            return

    await ctx.send(f"Congrats! you successfully bought {amount} {item}.")

@client.command(aliases = ['inventory'])
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = f":shopping_bags:  {user.name}'s Bag", colour = 0x00FF0C)
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = f"{amount}", inline = False)
        em.set_thumbnail(url = "https://media.discordapp.net/attachments/749996055369875459/751648770185494548/EP2.png")

    await ctx.send(embed = em)

async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]

    with open("moneybank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]

@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That item doesn't exist.")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1
        if t == None:
            return [False,3]
    except:
        return [False,3]

    with open("moneybank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]

@client.command(aliases=['donate', 'send'])
async def give(ctx, user:discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(discord.Member)

    if amount == None:
        await ctx.send("Please enter some amount lol")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount>bal[0]:
        await ctx.send("You don't enough money in your wallet.")
        return
    if amount<0:
        await ctx.send("You can't give negative money.")
        return

    await update_bank(ctx.author,-1*amount,"wallet")
    await update_bank(user,amount,"wallet")

    await ctx.send(f"Congrats! You successfully gave :coin: {amount} EpicCoins!")

async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("moneybank.json", "w") as f:
        json.dump(users, f)
    return True

async def get_bank_data():
    with open("moneybank.json", "r") as f:
        users = json.load(f)

    return users

async def update_bank(user, change = 0, mode = "wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("moneybank.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal

# Credits: Kaname
client.run(os.environ.get("BOT_TOKEN"))

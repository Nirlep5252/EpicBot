import discord 
import random
import asyncio
import aiohttp
import time
import datetime
from discord.ext import commands

class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def giveaway(self, ctx):
        def convert(time):
            pos = ["s", "m", "h", "d"]

            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}

            unit = time[-1]

            if unit not in pos:
                return -1
            try:
                val = int(time[:-1])
            except:
                return -2

            return val * time_dict[unit]

        await ctx.send(f"Let's start the giveaway! Insert some parameters to start the giveaway. Make sure you answer them within 30 seconds.")

        questions = ["Which channel should it be hosted in?",
                        "What should be the duration of the giveaway? (s|m|h|d)",
                        "What is the prize of the giveaway?"]

        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(i)

            try:
                msg = await self.client.wait_for("message", timeout = 30.0, check = check)
            except asyncio.TimeoutError:
                await ctx.send(f"You didn't answer in time, please try again later.")
                return
            else:
                answers.append(msg.content)

        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
            return

        channel = self.client.get_channel(c_id)

        time = convert(answers[1])
        if time == -1:
            await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time.")
            return
        elif time == -2:
            await ctx.send(f"The time must be an integer. Please enter an interger next time.")
            return
        prize = answers[2]

        await ctx.send(f"The Giveaway has begun in {channel.mention} and will last {answers[1]}.")


        user = ctx.author
        embed = discord.Embed(title = ":gift:  Giveaway  :gift:", color = 0x00FF0C)

        embed.add_field(name = "Giveaway Started By:", value = f"{user.mention}", inline = False)
        embed.add_field(name = "Prize:", value = f"{prize}", inline = False)
        embed.add_field(name = "Requirements:", value = f"React with   :gift:  to enter the Giveaway.")
        embed.set_footer(text = f"Ends {answers[1]} from now.")

        my_msg = await channel.send("🎉 Giveaway 🎉", embed = embed)

        await my_msg.add_reaction("🎁")

        await asyncio.sleep(time)

        new_msg = await ctx.channel.fetch_message(my_msg.id)

        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))

        winner = random.choice(users)

        await channel.send(f":partying_face: Congratulations :tada: {winner.mention}! You won the Giveaway.")

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def reroll(self, ctx, channel: discord.TextChannel, id_ : int):
        new_msg = await channel.fetch_message(id_)

        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))

        winner = random.choice(users)

        await channel.send(f":partying_face: Congratulations :tada: {winner.mention}! You won the Giveaway.")

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def announce(self, ctx):
        await ctx.send(f"Let's start the announcement! Insert some parameters to start the announcement. Make sure you answer them within 5 mins.")

        questions = ['Which channel should the announcement be in?',
                        'What should be the content of the announcement.',
                        'Are you sure you want to post this announcement? Type `yes` to confirm or type `no` to return.']

        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(i)

            try:
                msg = await self.client.wait_for("message", timeout = 300.0, check = check)
            except asyncio.TimeoutError:
                await ctx.send(f"You didn't answer in time, please try again later.")
                return
            else:
                answers.append(msg.content)

        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
            return

        channel = self.client.get_channel(c_id)

        announcement_content = answers[1]

        if answers[2].lower() == "no":
            await ctx.send(f"The announcement was cancelled.")
            return
        elif answers[2].lower() == "yes":
            await ctx.send(f"The announcement has been posted in {channel.mention}.")
            embed = discord.Embed(title = "**📢  Announcement  📢**", description = f"{announcement_content}", color = 0x00FF0C)
            embed.add_field(name = "Announced By:", value = f"{ctx.author.mention}", inline = False)
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.author.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await channel.send(embed = embed)
        else:
            await ctx.send(f"That's not a valid answer. Please try again later.")

    @commands.command()
    async def countdown(self, ctx, countdown_channel = None, author_time: str = None, *,topic = "Countdown"):
        if topic == None:
            topic == "Countdown"

        def convert(time):
            pos = ["s", "m", "h", "d"]

            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}

            unit = time[-1]

            if unit not in pos:
                return -1
            try:
                val = int(time[:-1])
            except:
                return -2

            return val * time_dict[unit]

        # both is not there
        if countdown_channel == None and author_time == None:
            await ctx.send(f"Let's start the countdown! Insert some parameters to start the countdown. Make sure you answer them within 30 seconds.")

            questions = ["Which channel should it be posted in?",
                            "What should be the duration of the countdown? (s|m|h|d)"]

            answers = []

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            for i in questions:
                await ctx.send(i)

                try:
                    msg = await self.client.wait_for("message", timeout = 30.0, check = check)
                except asyncio.TimeoutError:
                    await ctx.send(f"You didn't answer in time, please try again later.")
                    return
                else:
                    answers.append(msg.content)

            try:
                c_id = int(answers[0][2:-1])
            except:
                await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
                return

            channel = self.client.get_channel(c_id)

            time = convert(answers[1])
            if time == -1:
                await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time.")
                return
            elif time == -2:
                await ctx.send(f"The time must be an integer. Please enter an interger next time.")
                return

            await ctx.send(f"The Countdown has begun in {channel.mention} and will last {answers[1]}.")

            user = ctx.author

            embed = discord.Embed(title= f'{topic}', color=0x00FF0C, description= f"A Countdown has been started for {answers[1]}!\nThis Countdown was set by {user.mention}!\nYou can type `cancel` at any time to cancel the countdown!")
            embed.set_author(name = f"{user.name}", icon_url = f"{user.avatar_url}")

            await channel.send(embed=embed)
            def check2(message):
                return message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == "cancel"
            try:
                m = await self.client.wait_for("message", check=check2, timeout=time)
                em = discord.Embed(title = 'Countdown cancelled!', color=0xFF0000)

                await channel.send(embed=em)

            except asyncio.TimeoutError:
                emb = discord.Embed(title = f"Countdown Ended!", color = 0x00FF0C, description = f"The Countdown set for {answers[1]} set by {user.mention} has ended!")
                emb.set_author(name = f"{user.name}", icon_url = f"{user.avatar_url}")

                await channel.send(embed=emb)

        # both are there
        elif countdown_channel != None and author_time != None:
            try:
                c_id = int(countdown_channel[2:-1])
            except:
                await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
                return

            channel = self.client.get_channel(c_id)

            time = convert(author_time)
            if time == -1:
                await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time.")
                return
            elif time == -2:
                await ctx.send(f"The time must be an integer. Please enter an interger next time.")
                return

            await ctx.send(f"The Countdown has begun in {channel.mention} and will last {author_time}.")

            user = ctx.author

            embed = discord.Embed(title= f'{topic}', color=0x00FF0C, description= f"A Countdown has been started for {author_time}!\nThis Countdown was set by {user.mention}!\nYou can type `cancel` at any time to cancel the countdown!")
            embed.set_author(name = f"{user.name}", icon_url = f"{user.avatar_url}")

            await channel.send(embed=embed)
            def check2(message):
                return message.channel == ctx.channel and message.author == ctx.author and message.content.lower() == "cancel"
            try:
                m = await self.client.wait_for("message", check=check2, timeout=time)
                em = discord.Embed(title = 'Countdown cancelled!', color=0xFF0000)

                await channel.send(embed=em)

            except asyncio.TimeoutError:
                emb = discord.Embed(title = f"{topic}", color = 0xFFA500, description = f"The Countdown set for {author_time} set by {user.mention} has ended!")
                emb.set_author(name = f"{user.name}", icon_url = f"{user.avatar_url}")

                await channel.send(embed=emb)

def setup(client):
    client.add_cog(Giveaway(client))

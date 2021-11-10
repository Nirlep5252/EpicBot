import discord
import asyncio
import time
import random
from utils.time import convert
from discord.ext import commands
from utils.bot import EpicBot
from utils.embed import success_embed, error_embed
from config import MAIN_COLOR, EMOJIS
 
# this are for the dumb kids only
# uwu
 
class giveaway(commands.Cog, description="All the commands related to Giveaway!"):
    def __init__(self, client: EpicBot):
        self.client = client
        self.setup_timeout = 60.0 # How many seconds until the setup cancels due to no information being sent
        self.react_emoji = "🎉" # The emoji the user has to react with to enter the giveaway - Unicode

    @commands.group(aliases=['giveawaycommand', 'giveaway-command', 'giveawaycmd'], help="help in starting giveaways in ur server.")
    @commands.cooldown(3, 30, commands.BucketType.user)
    async def giveaway(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(ctx.command)

    @giveaway.command(name="create", help="start a giveaway with a wizard!")
    @commands.has_permissions(manage_guild = True)
    async def create(self, ctx: commands.Context):
        def sussy(time):
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

        timeout = self.setup_timeout
        embedq1 = discord.Embed(title=f"{EMOJIS['giveaway_']} | Giveaway Wizard",
                                description=f"Welcome to the Giveaway Wizard. Answer the following questions within `{timeout}` Seconds!",
                                color=MAIN_COLOR)
        embedq1.add_field(name=f"{EMOJIS['giveaway_']} | Question 1",
                          value="Where should we host the Giveaway?\n\n **Example**: ```py\n#General, #Bot-Command, #Giveaway\n```")
        embedq2 = discord.Embed(title=f"{EMOJIS['giveaway_']} | Giveaway Wizard",
                                description="Great! Let's move onto the next question.",
                                color=MAIN_COLOR)
        embedq2.add_field(name=f"{EMOJIS['giveaway_']} | Question 2",
                          value="How long should it last? `< s | m | h | d | w>`\n\n **Example**:\n `1d`")
        embedq3 = discord.Embed(title=f"{EMOJIS['giveaway_']} | Giveaway Wizard",
                                description="Awesome. Let's move onto the next question!",
                                color=MAIN_COLOR)
        embedq3.add_field(name=f"{EMOJIS['giveaway_']} | Question 3",
                          value="What is the prize the winner will receive?\n\n **Example**:\n ```css\nNitro, Discord Game, Movies, etc.\n```")

        embedq4 = discord.Embed(title=f"{EMOJIS['giveaway_']} | Giveaway Wizard",
                                description="Amazing. You've made it to the last question!",
                                color=MAIN_COLOR)
        embedq4.add_field(name=f"{EMOJIS['giveaway_']} | Question 4",
                          value="will I ping the winner?\n\n `yes \ no`")


        questions = [embedq1,
                     embedq2,
                     embedq3,
                     embedq4]

        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(embed=i)

            try:
                msg = await self.client.wait_for('message', timeout=self.setup_timeout, check=check)
            except asyncio.TimeoutError:
                embed = discord.Embed(title=f"{EMOJIS['giveaway_']} **Giveaway Setup Wizard**",
                                      description=":x: You didn't answer in time!")
                await ctx.send(embed=embed)
                return
            else:
                answers.append(msg.content)

        try:
            c_id = int(answers[0][2: -1])
        except:
            embed = discord.Embed(title=f"{EMOJIS['giveaway_']} **Giveaway Setup Wizard**",
                                  description=":x: You didn't specify a channel correctly!")
            await ctx.send(embed=embed)
            return

        channel = self.client.get_channel(c_id)

        timesus = sussy(answers[1])
        time_ = convert(answers[1])
        ping_the_winner = str(answers[3])
        if ping_the_winner not in ["yes", "no"]:
          return await ctx.send("you have not given the correct option!")
        if time_ == -1:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Unit of time.",
                f"Please enter a valid unit of time.\nValid units are: `s, m, h, d, w, y`\nExample: {example}"
            ))
        if time_ == -2:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Invalid Args!",
                f"The time argument should be an integer followed by a unit.\nExample: {example}"
            ))
        if time_ == -3:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Positive values only!",
                "The value of time should be positive values only."
            ))

        prize = answers[2]
        time_in_seconds = time_[0]
        if time_in_seconds > 43200 * 60 * 12 * 5:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply(embed=error_embed(
                f"{EMOJIS['tick_no']} Too long!",
                "Giveaway can't be longer than **5 years**."
            ))

        embed = discord.Embed(title=f"{EMOJIS['giveaway_']} **Giveaway Setup Wizard**",
                              description="Okay, all set. The Giveaway will now begin!",
                              color=MAIN_COLOR)
        embed.add_field(name="Hosted Channel:", value=f"{channel.mention}")
        embed.add_field(name="Time:", value=f"<t:{round(time.time() + time_in_seconds)}:R>")
        embed.add_field(name="Prize:", value=prize)
        await ctx.send(embed=embed)

        embed = discord.Embed(title=f"{EMOJIS['giveaway_']} | **{prize}**",
                              description = f"React with {self.react_emoji} to enter!\nTime Remaining: <t:{round(time.time() + time_in_seconds)}:R>\nHosted by - {ctx.author.mention}",
                              color=MAIN_COLOR)
        msg = await channel.send(embed=embed)

        await msg.add_reaction(self.react_emoji)
        await asyncio.sleep(timesus)

        new_msg = await channel.fetch_message(msg.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))

        winner = random.choice(users)
        if ping_the_winner == "yes":
            await msg.reply(f"{EMOJIS['giveaway_']} | The winner of `{prize}` is: || {winner.mention} ||", allowed_mentions=discord.AllowedMentions( users=True, everyone=False, roles=False, replied_user=False))

        embed2 = discord.Embed(title=f"{EMOJIS['giveaway_']} | **{prize}**",
                               description=f":trophy: **Winner:** {winner.mention}")
        embed2.set_footer(text="Giveaway Has Ended")
        await msg.edit(embed=embed2)




    @commands.command(aliases=['rroll'], help="reroll the giveaway!")
    @commands.has_permissions(manage_guild = True)
    async def reroll(self, ctx, channel: discord.TextChannel, message_id: int):
        try:
            new_msg = await channel.fetch_message(message_id)
            users = await new_msg.reactions[0].users().flatten()
            users.pop(users.index(self.client.user))
            winner = random.choice(users)
            await ctx.channel.send(f"{EMOJIS['giveaway_']} The new winner is: || {winner.mention} ||!", allowed_mentions=discord.AllowedMentions( users=True, everyone=False, roles=False, replied_user=False))
        except Exception as e:
            print(f"{e}")

def setup(client):
    client.add_cog(giveaway(client))

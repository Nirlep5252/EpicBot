"""
Copyright 2021 Nirlep_5252_
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import discord.ui
import asyncio
from config import MAIN_COLOR, EMPTY_CHARACTER
import random
from utils.embed import success_embed, error_embed
from discord.ext import commands
from utils.message import wait_for_msg
from games import tictactoe, wumpus, minesweeper, twenty
from utils.bot import EpicBot
from utils.message import wait_for_msg
from Discord_Games import aki_buttons

class TruthAndDareView(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="Dare", custom_id='dare', style=discord.ButtonStyle.danger)
    async def dare(self, button, interaction):
        self.value = 'dare'
        self.stop()

    @discord.ui.button(label="Truth", custom_id='truth', style=discord.ButtonStyle.green)
    async def truth(self, button, interaction):
        self.value = 'truth'
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id == self.ctx.author.id:
            return True
        return await interaction.response.send_message("This isn't your command!", ephemeral=True)


class games(commands.Cog, description="Play some fun games with me!"):
    def __init__(self, client: EpicBot):
        self.client = client

    @commands.command(aliases=['aki'], help="Play akinator!")
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, commands.BucketType.user)
    async def akinator(self, ctx):
        await aki_buttons.BetaAkinator().start(ctx, color=MAIN_COLOR)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name='2048', help="Play 2048 game.")
    async def twenty(self, ctx):
        await twenty.play(ctx, self.client)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='minesweeper', help="Play Minesweeper")
    async def minesweeper(self, ctx, columns=None, rows=None, bombs=None):
        await minesweeper.play(ctx, columns, rows, bombs)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='wumpus', help="Play Wumpus game")
    async def _wumpus(self, ctx):
        await wumpus.play(self.client, ctx)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['ttt', 'tic-tac-toe'], help="Play Tic-Tac-Toe")
    async def tictactoe(self, ctx):
        await tictactoe.play_game(self.client, ctx, chance_for_error=0.2)  # Win Plausible

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='rps', aliases=['rockpaperscissors'], help="Play Rock, Paper, Scissors game")
    async def rps(self, ctx):
        def check_win(p, b):
            if p == '🌑':
                return False if b == '📄' else True
            if p == '📄':
                return False if b == '✂' else True
            # p=='✂'
            return False if b == '🌑' else True

        async with ctx.typing():
            reactions = ['🌑', '📄', '✂']
            game_message = await ctx.send("**Rock Paper Scissors**\nChoose your shape:", delete_after=15.0)
            for reaction in reactions:
                await game_message.add_reaction(reaction)
            bot_emoji = random.choice(reactions)

        def check(reaction, user):
            return user != self.client.user and user == ctx.author and (str(reaction.emoji) == '🌑' or '📄' or '✂')
        try:
            reaction, _ = await self.client.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Time's Up! :stopwatch:")
        else:
            await ctx.send(f"**Your Choice:\t{reaction.emoji}\nMy Choice:\t{bot_emoji}**")
            # if conds
            if str(reaction.emoji) == bot_emoji:
                await ctx.send("**It's a Tie :ribbon:**")
            elif check_win(str(reaction.emoji), bot_emoji):
                await ctx.send("**You win :sparkles:**")
            else:
                await ctx.send("**I win :robot:**")

# this isn't the perfect edition
# I wanted to make a system in which the bot check if the message contains any attachments
# then it will send the final message of the dare part
# if ur good in Koding then make a good one urself

    @commands.command(aliases=['tnd'], help="Play truth and dare!")
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.max_concurrency(1, commands.BucketType.user)
    async def truth(self, ctx: commands.Context):
        view = TruthAndDareView(ctx)
        main_msg = await ctx.reply("Pick what u want to do?", view=view)
        await view.wait()
        if not view.value:
            return await main_msg.edit(content="Command cancelled or timed out!", view=None)
        if view.value == 'truth':
            truth_is_always_painful = random.choice([
                 "When was the last time you lied?",
                 "When was the last time you cried?",
                 "What's your biggest fear?",
                 "What's your biggest fantasy?",
                 "Do you have any fetishes?",
                 "What's something you're glad your mum doesn't know about you?",
                 "Have you ever cheated on someone?",
                 "What's the worst thing you've ever done?",
                 "What's a secret you've never told anyone?",
                 "Do you have a hidden talent?",
                 "Who was your first celebrity crush?",
                 "What are your thoughts on polyamory?",
                 "What's the worst intimate experience you've ever had?",
                 "Have you ever cheated in an exam?",
                 "What's the most drunk you've ever been?",
                 "Have you ever broken the law?",
                 "What's the most embarrassing thing you've ever done?",
                 "What's your biggest insecurity?",
                 "What's the biggest mistake you've ever made?",
                 "What's the most disgusting thing you've ever done?",
                 "Who would you like to kiss in this room?",
                 "What's the worst thing anyone's ever done to you?",
                 "Have you ever had a run in with the law?",
                 "What's your worst habit?",
                 "What's the worst thing you've ever said to anyone?",
                 "Have you ever peed in the shower?",
                 "What's the strangest dream you've had?",
                 "Have you ever been caught doing something you shouldn't have?",
                 "What's the worst date you've been on?",
                 "What's your biggest regret?",
                 "What's the biggest misconception about you?",
                 "Where's the weirdest place you've had sex?",
                 "Why did your last relationship break down?",
                 "Have you ever lied to get out of a bad date?",
                 "What's the most trouble you've been in?"])
            await main_msg.edit(content=f"```\n{truth_is_always_painful}\n```", view=None)
            msg_check = await wait_for_msg(ctx, 60, main_msg)
            if msg_check == 'pain':
                return
            else:
                await main_msg.edit(content="Oh, is that so? 😏 I didn't knew that. **Shame! Shame!**", view=None)
        elif view.value == 'dare':
            dare_is_more_and_always_painful = random.choice([
                 "Show the most embarrassing photo on your phone",
                 "Show the last five people you texted and what the messages said",
                 "Let the rest of the group DM someone from your Instagram account",
                 "Eat a raw piece of garlic",
                 "Do 100 squats",
                 "Keep three ice cubes in your mouth until they melt",
                 "Say something dirty to the person on your left",
                 "Give a foot massage to the person on your right",
                 "Put 10 different available liquids into a cup and drink it",
                 "Yell out the first word that comes to your mind",
                 "Give a lap dance to someone of your choice",
                 "Remove four items of clothing",
                 "Like the first 15 posts on your Facebook newsfeed",
                 "Eat a spoonful of mustard",
                 "Keep your eyes closed until it's your go again",
                 "Send a sext to the last person in your phonebook",
                 "Show off your orgasm face",
                 "Seductively eat a banana",
                 "Empty out your wallet/purse and show everyone what's inside",
                 "Do your best sexy crawl",
                 "Pretend to be the person to your right for 10 minutes",
                 "Eat a snack without using your hands",
                 "Say two honest things about everyone else in the group",
                 "Twerk for a minute",
                 "Try and make the group laugh as quickly as possible",
                 "Try to put your whole fist in your mouth",
                 "Tell everyone an embarrassing story about yourself",
                 "Try to lick your elbow",
                 "Post the oldest selfie on your phone on Instagram Stories",
                 "Tell the saddest story you know",
                 "Howl like a wolf for two minutes",
                 "Dance without music for two minutes",
                 "Pole dance with an imaginary pole",
                 "Let someone else tickle you and try not to laugh",
                 "Put as many snacks into your mouth at once as you can"])
            await main_msg.edit(content=f"```\n{dare_is_more_and_always_painful}\n```", view=None)
            msg_check = await wait_for_msg(ctx, 60, main_msg)
            if msg_check == 'pain':
                return
            else:
                await main_msg.edit(content="Oh, seems like u have some guts. Well done.", view=None)

def setup(client):
    client.add_cog(games(client))

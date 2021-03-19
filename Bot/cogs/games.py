import discord
import datetime
import random 
import asyncio
from discord.ext import commands
from games import tictactoe, wumpus, minesweeper, twenty
from config import *

class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='2048')
    async def twenty(self, ctx):
        """Play 2048 game"""
        await twenty.play(ctx, self.client)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='minesweeper', aliases=['ms'])
    async def minesweeper(self, ctx, columns = None, rows = None, bombs = None):
        """Play Minesweeper"""
        await minesweeper.play(ctx, columns, rows, bombs)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='wumpus')
    async def _wumpus(self, ctx):
        """Play Wumpus game"""
        await wumpus.play(self.client, ctx)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['randomno', 'random_number'])
    async def randomnumber(self, ctx, num1: int, num2: int):
        embed = discord.Embed(title = "Random Number Generator", description = (random.randint(num1 + 1, num2 - 1)), color = 0x00FF0C)
        await ctx.send(embed = embed)


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Roll a dice!")
    async def dice(self, ctx):
        embed = discord.Embed(
            title = "Rolling Dice...",
            color = MAIN_COLOR
        )
        msg = await ctx.message.reply(embed=embed)

        embed = discord.Embed(
            title = "Dice!",
            description=f"You rolled a **{random.randint(1, 6)}**",
            color = MAIN_COLOR
        )

        await msg.edit(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['answer', '8ball'])
    async def predict(self, ctx, *, question):
        responses = ['Yes. <a:EpicTick:760828595823837194>', 'No. <a:EpicCross:760830174207016980>', 'Probably. ', 'Maybe.', 'IDK bro ', 'Seems like it.', 'Nahh.', 'Oh hell yeah.', 'Yes Definitely.', 'I Think not', 'lol no bro', 'Concentrate and ask again', 'Ask a better question lol', 'Umm Yes', 'Umm No', 'Yes lmao', 'No, but imagine if it was yes lol', 'Yes, but imagine if it was no lol', 'hmm, good question', 'Yes, obviously', 'Definitely not']
        embed = discord.Embed(title = f"**:man_detective:  Prediction**", color = 0x00FF0C)
        embed.add_field(name = f"Question Asked:", value = f"{question}", inline = False)
        embed.add_field(name = f"Predicted Answer:", value = f"{random.choice(responses)}", inline = False)
        await ctx.send(embed = embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Flip a coin!", aliases=['coin', 'flip'])
    async def coinflip(self, ctx):
        outcomes = ['Heads', 'Tails']

        embed=discord.Embed(
            title = "Flipping the Coin...",
            color = MAIN_COLOR
        )
        msg = await ctx.message.reply(embed=embed)
        
        embed=discord.Embed(
            title=f"Coin!",
            description=f"Result: **{random.choice(outcomes)}**",
            color=MAIN_COLOR
        )
        await msg.edit(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='rps', aliases=['rockpaperscissors'])
    async def rps(self, ctx):
        """Play Rock, Paper, Scissors game"""
        def check_win(p, b):
            if p=='🌑':
                return False if b=='📄' else True
            if p=='📄':
                return False if b=='✂' else True
            # p=='✂'
            return False if b=='🌑' else True

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

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['ttt', 'tic-tac-toe'])
    async def tictactoe(self, ctx):
        """Play Tic-Tac-Toe"""
        await tictactoe.play_game(self.client, ctx, chance_for_error=0.2) # Win Plausible

def setup(client):
    client.add_cog(Games(client))
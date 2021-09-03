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

import asyncio
from config import MAIN_COLOR
import random
from discord.ext import commands
from games import tictactoe, wumpus, minesweeper, twenty
from utils.bot import EpicBot
from Discord_Games import aki_buttons


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


def setup(client):
    client.add_cog(games(client))

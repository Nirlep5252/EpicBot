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

import discord
import asyncio
import random
from discord.ext import commands
from games import tictactoe, wumpus, minesweeper, twenty
from Discord_Games import aki_buttons
from utils.bot import EpicBot
from utils.message import wait_for_msg
from utils.ui import BasicView
from games.snake import Score, Game, Emoji
from config import MAIN_COLOR


class TruthAndDareView(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    @discord.ui.button(label="Dare", custom_id='dare', style=discord.ButtonStyle.danger)
    async def dare(self, button, interaction):
        self.value = 'dare'
        self.stop()

    @discord.ui.button(label="Truth", custom_id='truth', style=discord.ButtonStyle.green)
    async def truth(self, button, interaction):
        self.value = 'truth'
        self.stop()


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

    @commands.command(aliases=['tnd', 'dare', 'truth', 'tod'], help="Play truth and dare!")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def truthordare(self, ctx: commands.Context):
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
                "What's the most trouble you've been in?"
            ])
            await main_msg.edit(content=f"```\n{truth_is_always_painful}\n```", view=None)
            msg_check = await wait_for_msg(ctx, 60, main_msg)
            if msg_check == 'pain':
                return
            else:
                await main_msg.edit(content="Oh, is that so? 😏 I didn't know that. **Shame! Shame!**", view=None)
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
                "Put as many snacks into your mouth at once as you can"
            ])
            await main_msg.edit(content=f"```\n{dare_is_more_and_always_painful}\n```", view=None)
            msg_check = await wait_for_msg(ctx, 60, main_msg)
            if msg_check == 'pain':
                return
            else:
                await main_msg.edit(content="Oh, seems like u have some guts. Well done.", view=None)

    @commands.command(help="Starts a game of Snake!")
    async def snake(self, ctx, size_x=10, size_y=10):
        # MAX SIZE IN NORMAL MESSAGE: 198 emojis (18 x 11)
        # MIN SIZE OF 5, BECAUSE OTHERWISE IT IS SMALL
        if size_x > 18:
            size_x = 18
        elif size_x < 5:
            size_x = 5
        if size_y > 11:
            size_y = 11
        elif size_y < 5:
            size_y = 5

        game = Game(size_x, size_y, ctx, self.client)
        await game.play()
        print('Game Ended.')

    @commands.command(help="Displays your personnal best in a given size, or all of them in Snake.")
    async def personnalbest(self, ctx, size_x: int = None, size_y: int = None):
        str_best = []
        dict_best = {}
        if size_x is None and size_y is None:
            for size in Score.high_scores.keys():
                try:
                    score = Score.high_scores[size][ctx.author.id]
                    str_best.append(f'**{size[0]}x{size[1]}**: {score}')
                    dict_best[f'{size[0]}x{size[1]}'] = score
                except KeyError as e:
                    # KeyError on user ID.
                    pass
        elif size_x is None or size_y is None:
            await ctx.send('Use either both `size_x` and `size_y`, or none.')
            return
        else:
            try:
                score = Score.high_scores[(size_x, size_y)][ctx.author.id]
                str_best.append(f'**{size_x}x{size_y}**: {score}')
                dict_best[f'{size_x}x{size_y}'] = score
            except KeyError as e:
                pass

        if len(str_best) == 0:
            str_best = ['No high scores registered yet.']

        e = discord.Embed(
            title='A Game of Snake',
            description='Personnal Best',
            type='rich',
            url='https://github.com/Nirlep5252/EpicBot',
            color=MAIN_COLOR,
        ).set_author(
            name=ctx.author.name,
            icon_url=ctx.author.display_avatar.url,
        ).set_footer(
            text='snekkkkk',
        )
        if len(dict_best) != 0:
            for s in dict_best:
                e.add_field(
                    name=s,
                    value=dict_best[s],
                )
        else:
            e.add_field(
                name='No high scores registered yet.',
                value='Start a game with `e!play`.',
            )

        await ctx.send(embed=e)


    @commands.command(aliases=['highscores'], help="Displays the top players and scores in a given size, or all of them in Snake")
    async def highscore(self, ctx, size_x: int = None, size_y: int = None):
        dict_top = {}
        if size_x is None and size_y is None:
            for size in Score.high_scores.keys():
                top_users = Score.get_top_users(size)
                score = Score.get_top(size)
                dict_top[f'{size[0]}x{size[1]} ({score})'] = \
                    '\n'.join(self.client.get_user(uid).display_name \
                    for uid in top_users)
        elif size_x is None or size_y is None:
            await ctx.send('Use either both `size_x` and `size_y`, or none.')
            return
        else:
            top_users = Score.get_top_users((size_x, size_y))
            score = Score.get_top((size_x, size_y))
            dict_top[f'{size_x}x{size_y} ({score})'] = \
                '\n'.join(self.client.get_user(uid).display_name \
                for uid in top_users)

        e = discord.Embed(
            title='A Game of Snake',
            description='High Scores',
            type='rich',
            url='https://github.com/Nirlep5252/EpicBot',
            color=MAIN_COLOR,
        ).set_footer(
            text='snek',
        )
        if len(dict_top) != 0:
            for s in dict_top:
                e.add_field(
                    name=s,
                    value=dict_top[s],
                )
        else:
            e.add_field(
                name='No high scores registered yet.',
                value='Start a game with `e!play`.',
            )

        await ctx.send(embed=e)


def setup(client):
    client.add_cog(games(client))

import discord
import datetime
import random 
import asyncio 
from discord.ext import commands
from games import tictactoe 

class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['randomno', 'random_number'])
    async def randomnumber(self, ctx, num1: int, num2: int):
        embed = discord.Embed(title = "Random Number Generator", description = (random.randint(num1 + 1, num2 - 1)), color = 0x00FF0C)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['dice', 'rolldice', 'roll'])
    async def roll_dice(self, ctx):
        user = ctx.author
        embed = discord.Embed(title = " :game_die:  Dice", description = f"Hey {user.mention}, you rolled a **{(random.randint(1, 6))}**", color = 0x00FF0C)
        await ctx.send(embed = embed)
        embed.set_footer(text=f"{user.guild}", icon_url=f"{user.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

    @commands.command(aliases=['answer', '8ball'])
    async def predict(self, ctx, *, question):
        responses = ['Yes. <a:EpicTick:760828595823837194>', 'No. <a:EpicCross:760830174207016980>', 'Probably. ', 'Maybe.', 'IDK bro ', 'Seems like it.', 'Nahh.', 'Oh hell yeah.', 'Yes Definitely.', 'I Think not', 'lol no bro', 'Concentrate and ask again', 'Ask a better question lol', 'Umm Yes', 'Umm No', 'Yes lmao', 'No, but imagine if it was yes lol', 'Yes, but imagine if it was no lol', 'hmm, good question', 'Yes, obviously', 'Definitely not']
        embed = discord.Embed(title = f"**:man_detective:  Prediction**", color = 0x00FF0C)
        embed.add_field(name = f"Question Asked:", value = f"{question}", inline = False)
        embed.add_field(name = f"Predicted Answer:", value = f"{random.choice(responses)}", inline = False)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['coin', 'coinflip', 'flipcoin'])
    async def flip(self, ctx):
        CoinChances = ['Heads 🎈', 'Tails 🎁', 'Heads 🎀', 'Tails 💎', 'Heads ✅', 'Tails ✅', 'Heads 🎉', 'Tails 🥁', 'Heads ✨', 'Tails 🎄']
        await ctx.send(f'{random.choice(CoinChances)}')

    # this cmd is the ugliest shit ever, please dont use this
    @commands.command()
    async def rps(self, ctx, selection: str = None):
        bot_chances = ['Rock :rock:', 'Paper 🧻', 'Scissors ✂']
        bot_selection = random.choice(bot_chances)

        if selection == None:
            await ctx.send(f"You didn't enter your selection, you have to use command like this - `e!rps [selection]`.\nSelections can only be rock paper or scissor.")
    # Bot selects Rock
        elif selection.lower() == "rock" and bot_selection == "Rock :rock:":
            embed = discord.Embed(title = "Rock, Paper and Scissors")
            embed.add_field(name = "Your Selection:", value = f"Rock :rock:", inline = False)
            embed.add_field(name = "EpicBot's Selection:", value = f"Rock :rock:", inline = False)
            embed.add_field(name = "Result", value = "Tie.", inline = False)
            await ctx.send(embed = embed)

        elif selection.lower() == "paper" and bot_selection == "Rock :rock:":
            embed = discord.Embed(title = "Rock, Paper and Scissors", color = 0x00FF0C)
            embed.add_field(name = "Your Selection:", value = f"Paper 🧻", inline = False)
            embed.add_field(name = "EpicBot's Selection:", value = f"Rock :rock:", inline = False)
            embed.add_field(name = "Result", value = "You won!", inline = False)
            await ctx.send(embed = embed)

        elif selection.lower() == "scissors" and bot_selection == "Rock :rock:":
            embed = discord.Embed(title = "Rock, Paper and Scissors", color = 0xFF0000)
            embed.add_field(name = "Your Selection:", value = f"Scissors ✂", inline = False)
            embed.add_field(name = "EpicBot's Selection:", value = f"Rock :rock:", inline = False)
            embed.add_field(name = "Result", value = "You Lost.", inline = False)
            await ctx.send(embed = embed)
    # Bot selects Paper
        elif selection.lower() == "rock" and bot_selection == "Paper 🧻":
            embed = discord.Embed(title = "Rock, Paper and Scissors", color = 0xFF0000)
            embed.add_field(name = "Your Selection:", value = f"Rock :rock:", inline = False)
            embed.add_field(name = "EpicBot's Selection:", value = f"Paper 🧻", inline = False)
            embed.add_field(name = "Result", value = "You Lost.", inline = False)
            await ctx.send(embed = embed)

        elif selection.lower() == "paper" and bot_selection == "Paper 🧻":
            embed = discord.Embed(title = "Rock, Paper and Scissors")
            embed.add_field(name = "Your Selection:", value = f"Paper 🧻", inline = False)
            embed.add_field(name = "EpicBot's Selection:", value = f"Paper 🧻", inline = False)
            embed.add_field(name = "Result", value = "Tie.", inline = False)
            await ctx.send(embed = embed)

        elif selection.lower() == "scissors" and bot_selection == "Paper 🧻":
            embed = discord.Embed(title = "Rock, Paper and Scissors", color = 0x00FF0C)
            embed.add_field(name = "Your Selection:", value = f"Scissors ✂", inline = False)
            embed.add_field(name = "EpicBot's Selection:", value = f"Paper 🧻", inline = False)
            embed.add_field(name = "Result", value = "You Won!", inline = False)
            await ctx.send(embed = embed)
    # Bot selects Scissors
        elif selection.lower() == "rock" and bot_selection == "Scissors ✂":
            embed = discord.Embed(title = "Rock, Paper and Scissors", color = 0x00FF0C)
            embed.add_field(name = "Your Selection:", value = f"Rock :rock:", inline = False)
            embed.add_field(name = "EpicBot's Selection:", value = f"Scissors ✂", inline = False)
            embed.add_field(name = "Result", value = "You Won!", inline = False)
            await ctx.send(embed = embed)

        elif selection.lower() == "paper" and bot_selection == "Scissors ✂":
            embed = discord.Embed(title = "Rock, Paper and Scissors", color = 0xFF0000)
            embed.add_field(name = "Your Selection:", value = f"Paper 🧻", inline = False)
            embed.add_field(name = "EpicBot's Selection:", value = f"Scissors ✂", inline = False)
            embed.add_field(name = "Result", value = "You Lost.", inline = False)
            await ctx.send(embed = embed)

        elif selection.lower() == "scissors" and bot_selection == "Scissors ✂":
            embed = discord.Embed(title = "Rock, Paper and Scissors")
            embed.add_field(name = "Your Selection:", value = f"Scissors ✂", inline = False)
            embed.add_field(name = "EpicBot's Selection:", value = f"Scissors ✂", inline = False)
            embed.add_field(name = "Result", value = "Tie.", inline = False)
            await ctx.send(embed = embed)
        else:
            await ctx.send(f"You didn't enter a valid selection. Please try again.")

    @commands.command(aliases=['ttt', 'tic-tac-toe'])
    async def tictactoe(self, ctx):
        """Play Tic-Tac-Toe"""
        await tictactoe.play_game(self.client, ctx, chance_for_error=0.2) # Win Plausible

def setup(client):
    client.add_cog(Games(client))

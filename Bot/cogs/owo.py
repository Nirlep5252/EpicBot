import discord 
import random
from discord.ext import commands 

class OWO(commands.Cog):
    def __init__(self, client):
        self.client = client

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

def setup(client):
    client.add_cog(OWO(client))
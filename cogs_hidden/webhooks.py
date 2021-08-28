from discord.ext import commands
from discord.utils import cached_property
from config import WEBHOOKS
from discord import Webhook


class Webhooks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cached_property
    def webhooks(self):
        final = {}
        for name, (id_, token) in WEBHOOKS.items():
            final[name] = Webhook.partial(id=id_, token=token, session=self.bot.session)
        return final


def setup(bot):
    bot.add_cog(Webhooks(bot))

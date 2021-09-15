from discord.ext import commands


class MusicGone(commands.CheckFailure):
    pass


class InvalidUrl(commands.BadArgument):
    def __init__(self, argument: str):
        self.argument = argument

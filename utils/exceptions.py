from discord.ext import commands


class MusicGone(commands.CheckFailure):
    pass


class InvalidUrl(commands.BadArgument):
    def __init__(self, argument: str):
        self.argument = argument


class InvalidAutomodModule(commands.BadArgument):
    def __init__(self, module: str):
        self.module = module


class AutomodModuleNotEnabled(commands.BadArgument):
    def __init__(self, module: str):
        self.module = module


class AutomodModuleAlreadyEnabled(commands.BadArgument):
    def __init__(self, module: str):
        self.module = module

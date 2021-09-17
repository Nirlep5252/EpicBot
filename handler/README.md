# App command handler

So you want to use my trash application commands handler? <br>
Well here are some things below that might help you, you can refer to all the code inside the `./handler` directory to get a better idea.

## Before you use:

You need to use my discord.py fork for this handler thing to work.
```bash
$ pip install -U git+https://github.com/Nirlep5252/discord.py
```

### Quick Example:

```py
from discord.ext import commands
from handler import InteractionClient, InteractionContext, slash_command, user_command, message_command

bot = commands.Bot(command_prefix="!")
InteractionClient(bot)  # important


@slash_command(help="A description for slash command.")  # the description is required for slash commands, you'll get error without it.
async def ping(ctx: InteractionContext):  # you need to type hint everything, literally everything.
    await ctx.reply("Pong!")
    #  You can also use `ctx.send` they both do the same thing.

@user_command(name="Slap")
async def slap(ctx: InteractionContext):
    # In a context menu command use `ctx.target` to get the target
    # For example, when a user command used on a user you can get `ctx.author` to get the person who used the command
    # and `ctx.target` to get the person on which the command was used on.
    await ctx.reply(f"{ctx.author.mention} slapped {ctx.target.mention}")

@message_command(name="Bookmark")
async def bookmark(ctx: InteractionContext):
    await ctx.reply(f"Bookmarked [this message]({ctx.target.jump_url})", ephemeral=True)


bot.run('token')
```

You can access all the app commands using the `bot.app_cmds` attribute.

### Cogs:

You need to have this in your `main.py` file or your bot file whatever that is.

```py
from discord.ext import commands
from handler import InteractionClient

bot = commands.Bot(command_prefix="!")
InteractionClient(bot)  # important

bot.run('token')
```

Your cog: 
```py
from discord.ext import commands
from handler import slash_command


class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(help="Pong!")
    async def ping(self, ctx: InteractionContext):  # DONT FORGET TYPE HINTING
        await ctx.reply("Pong!")


def setup(bot):
    bot.add_cog(ExampleCog(bot))
```

**⚠️ Important:** <br>
> Your cog attributes or cog methods will raise an `AttributeError` because this handler creates a fake cog class. (you can check using `type(self)`) <br>
> The only attributes for cogs that you will be able to access are `self.bot` and `self.client` <br>
> ^ This shouldn't be an issue for 90% of the users, but if you are one of the 10% who use this, you probably should'nt use this and you probably already know a workaround for that.

### How to add options in slash commands?

There are 3 ways of adding options.

1. Type hinting a supported type:
```py
import discord
from handler import slash_command, InteractionContext


@slash_command(help="Slash command with options")
async def bonk(ctx: InteractionContext, user: discord.Member, reason: str = "No reason provided"):
    # Here `user` will be a required arg since no default value is given
    # and `reason` will be a optional arg since a default value is provided
    await ctx.reply(f"{ctx.author.mention} bonked {user.mention} with reason {reason}")

```

2. Type hinting `SlashCommandOption` as a type:
```py
from handler import slash_command, InteractionContext
from handler import SlashCommandOption as Option


@slash_command(help="Slash command with options")
async def bonk(ctx: InteractionContext,
    user: Option(name="user", type=3, description="The user who you want to bonk.", required=True),
    reason: Option(name="reason", type=3, description="The reason why you want to bonk the user.", required=False) = "No reason provided"
):
    # type=3 means str, refer to the `handler/app_commands.py` file and the `slash_cmd_option_types` dict for more info on types.
    await ctx.reply(f"{ctx.author.mention} bonked {user.mention} with reason {reason}")

```

3. Pass the `options` kwarg in the `slash_command` decorator
```py
from handler import slash_command, InteractionContext
from handler import SlashCommandOption as Option


@slash_command(help="Slash command with options", options=[
    Option(name="user", type=3, description="The user who you want to bonk.", required=True),
    Option(name="reason", type=3, description="The reason why you want to bonk the user.", required=False)
]):
async def bonk(ctx: InteractionContext, user: discord.Member, reason: str = "No reason provided"):
    await ctx.reply(f"{ctx.author.mention} bonked {user.mention} with reason {reason}")
```

### There are also some extra events that you might wanna know about:

- `on_app_command` - When an application command is used. (args: `ctx`)
- `on_app_command_completion` - When an application command is used without any errors. (args: `ctx`)
- `on_app_command_error` - When an error occurs while using an application command. (args: `ctx`, `error`)
- `on_global_commands_update` - When global commands are updated. (args: `commands` - a list of all the commands payload) (this event is just for debug purposes)
- `on_guild_commands_update` - When guild commands are updated. (args: `commands` - a list of all the commands payload, `guild_id`) (this event is just for debug purposes)

### Important things to read before you spam my DMs:

- You need to load your cogs, before the bot logs in or before the `on_connect` event is triggered or else your cog application commands won't be registered.
- You need to provide a `help` kwarg for your slash commands, or they won't be registered.
- You need to use my fork of `discord.py` for this handler thing to work.
- Currently I'm the only one working on this handler thing and it's not really a public thing, so new features/bugs might take time to be added/fixed.
- The todo list thing can be found here for this handler: [click](https://github.com/Nirlep5252/EpicBot/projects/2#card-68504204)

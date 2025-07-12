from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from epicbot.plugins.base import BasePlugin

if TYPE_CHECKING:
    from epicbot.core.bot import EpicBot


class Plugin(BasePlugin):
    """Core commands plugin providing essential bot functionality."""

    def __init__(self, bot: "EpicBot") -> None:
        super().__init__(bot)
        self.name = "Core Commands"
        self.version = "1.0.0"
        self.description = "Essential bot commands like ping, info, and help"
        self.author = "EpicBot Team"

    async def setup(self) -> None:
        """Setup the core commands plugin."""
        await self.bot.add_cog(CoreCommands(self.bot))

    async def teardown(self) -> None:
        """Teardown the core commands plugin."""
        await self.bot.remove_cog("CoreCommands")


class CoreCommands(commands.Cog):
    """Core commands for EpicBot."""

    def __init__(self, bot: "EpicBot") -> None:
        self.bot = bot

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        """Check bot latency and response time."""
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Bot latency: {round(self.bot.latency * 1000)}ms",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="info")
    async def info(self, ctx: commands.Context) -> None:
        """Display bot information."""
        embed = discord.Embed(
            title="🤖 EpicBot Information",
            description="A modular Discord bot with plugin support",
            color=discord.Color.blue(),
        )

        embed.add_field(name="Guilds", value=len(self.bot.guilds), inline=True)

        embed.add_field(name="Users", value=len(self.bot.users), inline=True)

        embed.add_field(
            name="Loaded Plugins",
            value=len(self.bot.plugin_manager.get_loaded_plugins()),
            inline=True,
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="help")
    async def help_command(
        self, ctx: commands.Context, command: str | None = None
    ) -> None:
        """Display help information for commands."""
        if command is None:
            embed = discord.Embed(
                title="📚 EpicBot Help",
                description="Use `!help <command>` or `/help <command>` for specific command help",
                color=discord.Color.purple(),
            )

            for cog_name, cog in self.bot.cogs.items():
                # Filter commands that the user can actually run
                accessible_commands = []
                for cmd in cog.get_commands():
                    try:
                        # Check if user can run this command
                        if await cmd.can_run(ctx):
                            accessible_commands.append(cmd.name)
                    except commands.CommandError:
                        # If can_run raises an error, user can't run the command
                        continue

                if accessible_commands:
                    embed.add_field(
                        name=cog_name,
                        value=", ".join(accessible_commands),
                        inline=False,
                    )

            await ctx.send(embed=embed)
        else:
            cmd = self.bot.get_command(command)
            if cmd is None:
                await ctx.send(f"Command `{command}` not found.")
                return

            # Check if user can run this specific command
            try:
                if not await cmd.can_run(ctx):
                    await ctx.send(f"You don't have permission to use `{command}`.")
                    return
            except commands.CommandError:
                await ctx.send(f"You don't have permission to use `{command}`.")
                return

            embed = discord.Embed(
                title=f"Help: {cmd.name}",
                description=cmd.help or "No description available",
                color=discord.Color.purple(),
            )

            if cmd.usage:
                prefix = "!" if ctx.prefix else "/"
                embed.add_field(
                    name="Usage",
                    value=f"`{prefix}{cmd.name} {cmd.usage}`",
                    inline=False,
                )

            await ctx.send(embed=embed)

    @commands.hybrid_command(name="sync")
    @commands.is_owner()
    async def sync_commands(self, ctx: commands.Context) -> None:
        """Sync slash commands to Discord. (Bot owner only)"""
        try:
            synced = await self.bot.tree.sync()
            embed = discord.Embed(
                title="✅ Commands Synced",
                description=f"Successfully synced {len(synced)} command(s)",
                color=discord.Color.green(),
            )
        except Exception as e:
            embed = discord.Embed(
                title="❌ Sync Failed",
                description=f"Failed to sync commands: {e}",
                color=discord.Color.red(),
            )

        await ctx.send(embed=embed)

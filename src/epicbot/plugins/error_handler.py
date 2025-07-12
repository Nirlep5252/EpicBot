import logging
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from epicbot.plugins.base import BasePlugin

if TYPE_CHECKING:
    from epicbot.core.bot import EpicBot


class Plugin(BasePlugin):
    """Global error handler for all command types."""

    def __init__(self, bot: "EpicBot") -> None:
        super().__init__(bot)
        self.name = "Error Handler"
        self.version = "1.0.0"
        self.description = "Handles command errors gracefully"
        self.author = "EpicBot Team"

    async def setup(self) -> None:
        """Setup the error handler plugin."""
        await self.bot.add_cog(ErrorHandler(self.bot))

    async def teardown(self) -> None:
        """Teardown the error handler plugin."""
        await self.bot.remove_cog("ErrorHandler")


class ErrorHandler(commands.Cog):
    """Handles all command errors gracefully."""

    def __init__(self, bot: "EpicBot") -> None:
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Global error handler for both prefix and hybrid commands."""

        # If command has a local error handler, let it handle the error
        if hasattr(ctx.command, "on_error"):
            return

        # If the error was already handled by a local error handler
        if isinstance(error, commands.CommandInvokeError) and hasattr(
            error.original, "__handled__"
        ):
            return


        # Create embed for error response
        embed = discord.Embed(color=discord.Color.red())

        # Handle specific error types
        if isinstance(error, commands.CommandNotFound):
            # Silently ignore unknown commands to avoid spam
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            embed.title = "❌ Missing Required Argument"
            embed.description = (
                f"You're missing the required argument: `{error.param.name}`"
            )

            if ctx.command:
                # Show command usage
                prefix = ctx.prefix or "/"
                embed.add_field(
                    name="Usage",
                    value=f"`{prefix}{ctx.command.qualified_name} {self._get_command_signature(ctx.command)}`",
                    inline=False,
                )

        elif isinstance(error, commands.BadArgument):
            embed.title = "❌ Invalid Argument"
            embed.description = f"Invalid argument provided: {error!s}"

        elif isinstance(error, commands.TooManyArguments):
            embed.title = "❌ Too Many Arguments"
            embed.description = "You provided too many arguments for this command."

        elif isinstance(error, commands.MissingPermissions):
            embed.title = "❌ Missing Permissions"
            perms = ", ".join(error.missing_permissions)
            embed.description = (
                f"You need the following permissions to use this command: `{perms}`"
            )

        elif isinstance(error, commands.BotMissingPermissions):
            embed.title = "❌ Bot Missing Permissions"
            perms = ", ".join(error.missing_permissions)
            embed.description = (
                f"I need the following permissions to execute this command: `{perms}`"
            )

        elif isinstance(error, commands.NotOwner):
            embed.title = "❌ Access Denied"
            embed.description = "This command is restricted to the bot owner only."

        elif isinstance(error, commands.NoPrivateMessage):
            embed.title = "❌ Server Only Command"
            embed.description = (
                "This command can only be used in a server, not in direct messages."
            )

        elif isinstance(error, commands.PrivateMessageOnly):
            embed.title = "❌ DM Only Command"
            embed.description = "This command can only be used in direct messages."

        elif isinstance(error, commands.CommandOnCooldown):
            embed.title = "❌ Command on Cooldown"
            embed.description = f"This command is on cooldown. Try again in `{error.retry_after:.1f}` seconds."

        elif isinstance(error, commands.MaxConcurrencyReached):
            embed.title = "❌ Command Busy"
            embed.description = f"This command is already being used by {error.number} user(s). Please wait."

        elif isinstance(error, commands.DisabledCommand):
            embed.title = "❌ Command Disabled"
            embed.description = "This command is currently disabled."

        elif isinstance(error, commands.CheckFailure):
            embed.title = "❌ Check Failed"
            embed.description = "You don't have permission to use this command."

        elif isinstance(error, commands.ExtensionError):
            embed.title = "❌ Extension Error"
            embed.description = (
                "An error occurred with a bot extension. Please contact support."
            )

        else:
            # Log unexpected errors
            self.logger.error(
                f"Unexpected error in command {ctx.command}: {error}", exc_info=error
            )

            embed.title = "❌ Unexpected Error"
            embed.description = "An unexpected error occurred. Please try again later."

            # Add error details for debugging (only in debug mode)
            if self.bot.config.debug:
                embed.add_field(
                    name="Error Details",
                    value=f"```{str(error)[:500]}```",
                    inline=False,
                )

        # Add help information if available
        if ctx.command and embed.title != "❌ Unexpected Error":
            embed.add_field(
                name="Need Help?",
                value=f"Use `{ctx.prefix or '/'}help {ctx.command.qualified_name}` for more information.",
                inline=False,
            )

        # Send error message
        try:
            # For slash commands, we need to handle interaction responses
            if ctx.interaction and not ctx.interaction.response.is_done():
                await ctx.interaction.response.send_message(embed=embed, ephemeral=True)
            elif ctx.interaction and ctx.interaction.response.is_done():
                await ctx.interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await ctx.send(embed=embed)

        except discord.NotFound:
            # Interaction expired, try sending a regular message
            try:
                await ctx.send(embed=embed)
            except Exception:
                # If all else fails, log the error
                self.logger.error(
                    f"Failed to send error message for command {ctx.command}: {error}"
                )

    def _get_command_signature(self, command: commands.Command) -> str:
        """Generate a command signature showing required and optional parameters."""
        signature_parts = []

        for param in command.params.values():
            if param.name in ("self", "ctx"):
                continue

            if param.default is param.empty:
                # Required parameter
                signature_parts.append(f"<{param.name}>")
            else:
                # Optional parameter
                signature_parts.append(f"[{param.name}]")

        return " ".join(signature_parts)

    @commands.Cog.listener()
    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: discord.app_commands.AppCommandError,
    ) -> None:
        """Handle app command specific errors."""
        # Create a mock context for compatibility with on_command_error
        # This ensures hybrid commands use the same error handling
        if hasattr(interaction, "command") and hasattr(
            interaction.command, "qualified_name"
        ):
            # Log app command errors
            self.logger.error(
                f"App command error in {interaction.command.qualified_name}: {error}",
                exc_info=error,
            )

        # For pure app commands (non-hybrid), handle specific app command errors
        embed = discord.Embed(color=discord.Color.red())

        if isinstance(error, discord.app_commands.CommandNotFound):
            return  # Silently ignore

        elif isinstance(error, discord.app_commands.MissingPermissions):
            embed.title = "❌ Missing Permissions"
            perms = ", ".join(error.missing_permissions)
            embed.description = f"You need the following permissions: `{perms}`"

        elif isinstance(error, discord.app_commands.BotMissingPermissions):
            embed.title = "❌ Bot Missing Permissions"
            perms = ", ".join(error.missing_permissions)
            embed.description = f"I need the following permissions: `{perms}`"

        elif isinstance(error, discord.app_commands.CommandOnCooldown):
            embed.title = "❌ Command on Cooldown"
            embed.description = f"Try again in `{error.retry_after:.1f}` seconds."

        else:
            self.logger.error(f"Unexpected app command error: {error}", exc_info=error)
            embed.title = "❌ Unexpected Error"
            embed.description = "An unexpected error occurred. Please try again later."

        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            self.logger.error(f"Failed to send app command error message: {e}")

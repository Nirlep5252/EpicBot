from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from epicbot.plugins.base import BasePlugin

if TYPE_CHECKING:
    from epicbot.core.bot import EpicBot


class Plugin(BasePlugin):
    """Prefix management commands for guild administrators."""

    def __init__(self, bot: "EpicBot") -> None:
        super().__init__(bot)
        self.name = "Prefix Manager"
        self.version = "1.0.0"
        self.description = "Commands for managing guild prefixes"
        self.author = "EpicBot Team"

    async def setup(self) -> None:
        """Setup the prefix commands plugin."""
        await self.bot.add_cog(PrefixCommands(self.bot))

    async def teardown(self) -> None:
        """Teardown the prefix commands plugin."""
        await self.bot.remove_cog("PrefixCommands")


class PrefixCommands(commands.Cog):
    """Commands for managing guild prefixes."""

    def __init__(self, bot: "EpicBot") -> None:
        self.bot = bot

    @commands.hybrid_group(name="prefix", invoke_without_command=True)
    @commands.guild_only()
    async def prefix_group(self, ctx: commands.Context) -> None:
        """View current prefixes for this server."""
        if ctx.guild is None:
            return

        # Ensure guild exists in database
        await self.bot.guild_manager.ensure_guild_exists(ctx.guild.id, ctx.guild.name)

        # Get current prefixes
        prefixes = await self.bot.guild_manager.get_guild_prefixes(ctx.guild.id)

        embed = discord.Embed(
            title="🏷️ Server Prefixes",
            color=discord.Color.blue(),
        )

        if not prefixes:
            embed.description = "No custom prefixes set. Using default prefix: `!`"
        else:
            prefix_list = "\n".join(f"• `{prefix}`" for prefix in prefixes)
            embed.description = f"**Custom prefixes:**\n{prefix_list}"

        embed.add_field(
            name="Always Available",
            value="• Bot mention (@EpicBot)\n• In DMs: `!`",
            inline=False,
        )

        await ctx.send(embed=embed)

    @prefix_group.command(name="list")
    @commands.guild_only()
    async def list_prefixes(self, ctx: commands.Context) -> None:
        """List current prefixes for this server."""
        # Same functionality as the parent command
        await self.prefix_group(ctx)

    @prefix_group.command(name="add")
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def add_prefix(self, ctx: commands.Context, prefix: str) -> None:
        """Add a custom prefix for this server."""
        if ctx.guild is None:
            return

        # Validate prefix
        if len(prefix) > 10:
            embed = discord.Embed(
                title="❌ Invalid Prefix",
                description="Prefix must be 10 characters or less.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        if prefix.strip() != prefix or not prefix:
            embed = discord.Embed(
                title="❌ Invalid Prefix",
                description="Prefix cannot be empty or contain only whitespace.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        # Ensure guild exists
        await self.bot.guild_manager.ensure_guild_exists(ctx.guild.id, ctx.guild.name)

        # Check current prefix count (limit to prevent abuse)
        current_count = await self.bot.guild_manager.get_prefix_count(ctx.guild.id)
        if current_count >= 10:
            embed = discord.Embed(
                title="❌ Too Many Prefixes",
                description="Maximum of 10 custom prefixes allowed per server.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        # Add the prefix
        success = await self.bot.guild_manager.add_guild_prefix(ctx.guild.id, prefix)

        if success:
            embed = discord.Embed(
                title="✅ Prefix Added",
                description=f"Successfully added prefix: `{prefix}`",
                color=discord.Color.green(),
            )
        else:
            embed = discord.Embed(
                title="❌ Prefix Already Exists",
                description=f"The prefix `{prefix}` is already set for this server.",
                color=discord.Color.orange(),
            )

        await ctx.send(embed=embed)

    @prefix_group.command(name="remove")
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def remove_prefix(self, ctx: commands.Context, prefix: str) -> None:
        """Remove a custom prefix from this server."""
        if ctx.guild is None:
            return

        # Ensure guild exists
        await self.bot.guild_manager.ensure_guild_exists(ctx.guild.id, ctx.guild.name)

        # Remove the prefix
        success = await self.bot.guild_manager.remove_guild_prefix(ctx.guild.id, prefix)

        if success:
            embed = discord.Embed(
                title="✅ Prefix Removed",
                description=f"Successfully removed prefix: `{prefix}`",
                color=discord.Color.green(),
            )
        else:
            embed = discord.Embed(
                title="❌ Prefix Not Found",
                description=f"The prefix `{prefix}` is not set for this server.",
                color=discord.Color.orange(),
            )

        await ctx.send(embed=embed)

    @prefix_group.command(name="clear")
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def clear_prefixes(self, ctx: commands.Context) -> None:
        """Remove all custom prefixes from this server."""
        if ctx.guild is None:
            return

        # Ensure guild exists
        await self.bot.guild_manager.ensure_guild_exists(ctx.guild.id, ctx.guild.name)

        # Clear all prefixes
        removed_count = await self.bot.guild_manager.clear_guild_prefixes(ctx.guild.id)

        if removed_count > 0:
            embed = discord.Embed(
                title="✅ Prefixes Cleared",
                description=f"Successfully removed {removed_count} custom prefix(es). "
                f"Default prefix `!` and bot mentions are still available.",
                color=discord.Color.green(),
            )
        else:
            embed = discord.Embed(
                title="📋 No Prefixes to Clear",
                description="This server has no custom prefixes set.",
                color=discord.Color.blue(),
            )

        await ctx.send(embed=embed)

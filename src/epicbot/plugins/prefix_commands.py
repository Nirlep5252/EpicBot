from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from epicbot.plugins.base import BasePlugin

if TYPE_CHECKING:
    from epicbot.core.bot import EpicBot


class ConfirmDefaultPrefixRemovalView(discord.ui.View):
    """Confirmation view for removing the default prefix when no custom prefixes exist."""

    def __init__(self, bot: "EpicBot", guild_id: int):
        super().__init__(timeout=60.0)  # 1 minute timeout
        self.bot = bot
        self.guild_id = guild_id

    @discord.ui.button(
        label="Yes, disable it", style=discord.ButtonStyle.red, emoji="⚠️"
    )
    async def confirm_disable(
        self, interaction: discord.Interaction, _button: discord.ui.Button
    ):
        """Confirm disabling the default prefix."""
        # Disable default prefix
        await self.bot.guild_manager.set_default_prefix_enabled(self.guild_id, False)

        embed = discord.Embed(
            title="✅ Default Prefix Disabled",
            description="The default prefix `!` has been disabled for this server.\n"
            "Bot mentions will still work.",
            color=discord.Color.green(),
        )

        # Disable all buttons after interaction
        for item in self.children:
            if hasattr(item, "disabled"):
                item.disabled = True

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="No, keep it", style=discord.ButtonStyle.green, emoji="✅")
    async def cancel_disable(
        self, interaction: discord.Interaction, _button: discord.ui.Button
    ):
        """Cancel disabling the default prefix."""
        embed = discord.Embed(
            title="✅ Cancelled",
            description="The default prefix `!` will remain enabled for this server.",
            color=discord.Color.blue(),
        )

        # Disable all buttons after interaction
        for item in self.children:
            if hasattr(item, "disabled"):
                item.disabled = True

        await interaction.response.edit_message(embed=embed, view=self)

    async def on_timeout(self):
        """Called when the view times out."""
        # Disable all buttons when timeout occurs
        for item in self.children:
            if hasattr(item, "disabled"):
                item.disabled = True


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
        default_enabled = await self.bot.guild_manager.is_default_prefix_enabled(
            ctx.guild.id
        )

        embed = discord.Embed(
            title="🏷️ Server Prefixes",
            color=discord.Color.blue(),
        )

        prefix_parts = []

        if prefixes:
            custom_list = "\n".join(f"• `{prefix}`" for prefix in prefixes)
            prefix_parts.append(f"**Custom prefixes:**\n{custom_list}")

        if default_enabled:
            prefix_parts.append("**Default prefix:** `!`")

        if not prefix_parts:
            embed.description = (
                "⚠️ **No prefixes enabled!** Only bot mentions will work."
            )
        else:
            embed.description = "\n\n".join(prefix_parts)

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
        """Add a custom prefix for this server. Use '!' to enable the default prefix."""
        if ctx.guild is None:
            return

        # Handle special case for default prefix
        if prefix == "!":
            await self.bot.guild_manager.ensure_guild_exists(
                ctx.guild.id, ctx.guild.name
            )

            # Check if default prefix is already enabled
            default_enabled = await self.bot.guild_manager.is_default_prefix_enabled(
                ctx.guild.id
            )
            if default_enabled:
                embed = discord.Embed(
                    title="💡 Already Enabled",
                    description="The default prefix `!` is already enabled for this server.",
                    color=discord.Color.blue(),
                )
                await ctx.send(embed=embed)
                return

            # Enable default prefix
            await self.bot.guild_manager.set_default_prefix_enabled(ctx.guild.id, True)

            embed = discord.Embed(
                title="✅ Default Prefix Enabled",
                description="The default prefix `!` has been enabled for this server.",
                color=discord.Color.green(),
            )
            await ctx.send(embed=embed)
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
        """Remove a custom prefix from this server. Use '!' to disable the default prefix."""
        if ctx.guild is None:
            return

        # Handle special case for default prefix
        if prefix == "!":
            await self.bot.guild_manager.ensure_guild_exists(
                ctx.guild.id, ctx.guild.name
            )

            # Check if default prefix is already disabled
            default_enabled = await self.bot.guild_manager.is_default_prefix_enabled(
                ctx.guild.id
            )
            if not default_enabled:
                embed = discord.Embed(
                    title="💡 Already Disabled",
                    description="The default prefix `!` is already disabled for this server.",
                    color=discord.Color.blue(),
                )
                await ctx.send(embed=embed)
                return

            # Check if there are any custom prefixes or warn about only having mentions
            custom_prefixes = await self.bot.guild_manager.get_guild_prefixes(
                ctx.guild.id
            )
            if not custom_prefixes:
                embed = discord.Embed(
                    title="⚠️ Warning",
                    description="Disabling the default prefix without custom prefixes means only bot mentions will work!\n\n"
                    "Consider adding a custom prefix first with `/prefix add <prefix>`",
                    color=discord.Color.orange(),
                )
                embed.add_field(
                    name="Are you sure?",
                    value="Choose below to confirm or cancel this action.",
                    inline=False,
                )

                # Create confirmation view with buttons
                view = ConfirmDefaultPrefixRemovalView(self.bot, ctx.guild.id)
                await ctx.send(embed=embed, view=view)
                return

            # Disable default prefix directly if custom prefixes exist
            await self.bot.guild_manager.set_default_prefix_enabled(ctx.guild.id, False)

            embed = discord.Embed(
                title="✅ Default Prefix Disabled",
                description="The default prefix `!` has been disabled for this server.\n"
                "Bot mentions will still work.",
                color=discord.Color.green(),
            )
            await ctx.send(embed=embed)
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

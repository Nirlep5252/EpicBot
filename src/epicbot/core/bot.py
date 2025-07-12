import logging

import discord
from discord.ext import commands

from epicbot.core.config import Config
from epicbot.database.connection import DatabaseManager
from epicbot.models.guild import GuildManager
from epicbot.plugins.manager import PluginManager


class EpicBot(commands.Bot):
    """Main Discord bot class with plugin support."""

    def __init__(self, config: Config):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True

        super().__init__(
            command_prefix=self._get_prefix, intents=intents, help_command=None
        )

        self.config = config
        self.logger = logging.getLogger(__name__)
        self.db_manager = DatabaseManager(config)
        self.guild_manager = GuildManager(self.db_manager)
        self.plugin_manager = PluginManager(bot=self)

    async def _get_prefix(
        self, bot: commands.Bot, message: discord.Message
    ) -> list[str] | str:
        """Dynamic prefix based on guild configuration."""
        # Default prefixes (always available)
        prefixes = [f"<@{self.user.id}> ", f"<@!{self.user.id}> "]  # Bot mentions

        # For DMs, only use mentions and default prefix
        if message.guild is None:
            prefixes.append("!")
            return prefixes

        # Get guild-specific prefixes
        try:
            guild_prefixes = await self.guild_manager.get_guild_prefixes(
                message.guild.id
            )
            if guild_prefixes:
                prefixes.extend(guild_prefixes)

            # Check if default prefix is enabled for this guild
            default_enabled = await self.guild_manager.is_default_prefix_enabled(
                message.guild.id
            )
            if default_enabled:
                prefixes.append("!")
        except Exception as e:
            self.logger.error(
                f"Error getting prefixes for guild {message.guild.id}: {e}"
            )
            prefixes.append("!")  # Fallback to default

        return prefixes

    async def on_ready(self) -> None:
        """Called when the bot is ready and connected to Discord."""
        self.logger.info(f"Bot is ready! Logged in as {self.user}")
        await self.plugin_manager.load_default_plugins()

        # Sync command tree for slash commands
        try:
            synced = await self.tree.sync()
            self.logger.info(f"Synced {len(synced)} command(s)")
        except Exception as e:
            self.logger.error(f"Failed to sync commands: {e}")

    async def on_guild_join(self, guild: discord.Guild) -> None:
        """Handle bot joining a new guild."""
        self.logger.info(f"Joined guild: {guild.name} (ID: {guild.id})")

        # Initialize guild in database
        try:
            await self.guild_manager.ensure_guild_exists(guild.id, guild.name)
            self.logger.info(f"Guild {guild.name} initialized in database")
        except Exception as e:
            self.logger.error(f"Failed to initialize guild {guild.name}: {e}")

        # TODO: Send welcome message to guild owner

    async def on_guild_remove(self, guild: discord.Guild) -> None:
        """Handle bot being removed from a guild."""
        self.logger.info(f"Removed from guild: {guild.name} (ID: {guild.id})")
        # TODO: Clean up guild data from database

    async def setup_hook(self) -> None:
        """Setup hook called during bot startup."""
        self.logger.info("Running setup hook...")
        await self.plugin_manager.initialize()

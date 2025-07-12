import logging

import discord
from discord.ext import commands

from epicbot.core.config import Config
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
        self.plugin_manager = PluginManager(bot=self)

    async def _get_prefix(self, bot: commands.Bot, message: discord.Message) -> str:
        """Dynamic prefix based on guild configuration."""
        # TODO: Implement per-guild prefix storage
        return "!"

    async def on_ready(self) -> None:
        """Called when the bot is ready and connected to Discord."""
        self.logger.info(f"Bot is ready! Logged in as {self.user}")
        await self.plugin_manager.load_default_plugins()

    async def on_guild_join(self, guild: discord.Guild) -> None:
        """Handle bot joining a new guild."""
        self.logger.info(f"Joined guild: {guild.name} (ID: {guild.id})")
        # TODO: Initialize guild in database
        # TODO: Send welcome message to guild owner

    async def on_guild_remove(self, guild: discord.Guild) -> None:
        """Handle bot being removed from a guild."""
        self.logger.info(f"Removed from guild: {guild.name} (ID: {guild.id})")
        # TODO: Clean up guild data from database

    async def setup_hook(self) -> None:
        """Setup hook called during bot startup."""
        self.logger.info("Running setup hook...")
        await self.plugin_manager.initialize()

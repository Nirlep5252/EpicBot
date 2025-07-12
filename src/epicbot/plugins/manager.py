import importlib.util
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from epicbot.plugins.base import BasePlugin

if TYPE_CHECKING:
    from epicbot.core.bot import EpicBot


class PluginManager:
    """Manages loading, unloading, and execution of plugins."""

    def __init__(self, bot: "EpicBot"):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.loaded_plugins: dict[str, BasePlugin] = {}
        self.plugin_directory = Path(bot.config.plugins_directory)

    async def initialize(self) -> None:
        """Initialize the plugin manager."""
        self.logger.info("Initializing plugin manager...")

        if not self.plugin_directory.exists():
            self.plugin_directory.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created plugins directory: {self.plugin_directory}")

    async def load_default_plugins(self) -> None:
        """Load core default plugins."""
        default_plugins = ["core_commands", "plugin_manager_commands"]

        for plugin_name in default_plugins:
            try:
                await self.load_plugin(plugin_name)
            except Exception as error:
                self.logger.error(
                    f"Failed to load default plugin {plugin_name}: {error}"
                )

    async def load_plugin(self, plugin_name: str) -> bool:
        """Load a specific plugin by name."""
        if plugin_name in self.loaded_plugins:
            self.logger.warning(f"Plugin {plugin_name} is already loaded")
            return False

        try:
            plugin_path = self.plugin_directory / f"{plugin_name}.py"

            if not plugin_path.exists():
                self.logger.error(f"Plugin file not found: {plugin_path}")
                return False

            # Dynamic import of plugin
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if spec is None or spec.loader is None:
                self.logger.error(f"Failed to create spec for plugin: {plugin_name}")
                return False

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Get the plugin class
            plugin_class = getattr(module, "Plugin", None)
            if plugin_class is None:
                self.logger.error(f"Plugin {plugin_name} does not have a Plugin class")
                return False

            # Instantiate and initialize plugin
            plugin_instance = plugin_class(self.bot)
            await plugin_instance.setup()

            self.loaded_plugins[plugin_name] = plugin_instance
            self.logger.info(f"Successfully loaded plugin: {plugin_name}")
            return True

        except Exception as error:
            self.logger.error(f"Failed to load plugin {plugin_name}: {error}")
            return False

    async def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a specific plugin by name."""
        if plugin_name not in self.loaded_plugins:
            self.logger.warning(f"Plugin {plugin_name} is not loaded")
            return False

        try:
            plugin = self.loaded_plugins[plugin_name]
            await plugin.teardown()
            del self.loaded_plugins[plugin_name]

            self.logger.info(f"Successfully unloaded plugin: {plugin_name}")
            return True

        except Exception as error:
            self.logger.error(f"Failed to unload plugin {plugin_name}: {error}")
            return False

    async def reload_plugin(self, plugin_name: str) -> bool:
        """Reload a specific plugin."""
        if plugin_name in self.loaded_plugins:
            await self.unload_plugin(plugin_name)

        return await self.load_plugin(plugin_name)

    def get_loaded_plugins(self) -> list[str]:
        """Get list of currently loaded plugin names."""
        return list(self.loaded_plugins.keys())

    def get_plugin(self, plugin_name: str) -> BasePlugin | None:
        """Get a loaded plugin instance by name."""
        return self.loaded_plugins.get(plugin_name)

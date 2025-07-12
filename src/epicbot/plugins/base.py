from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from epicbot.core.bot import EpicBot


class BasePlugin(ABC):
    """Base class for all EpicBot plugins."""

    def __init__(self, bot: "EpicBot"):
        self.bot = bot
        self.name = self.__class__.__name__
        self.version = "1.0.0"
        self.description = "A plugin for EpicBot"
        self.author = "Unknown"
        self.enabled = True

    @abstractmethod
    async def setup(self) -> None:
        """Setup the plugin. Called when the plugin is loaded."""
        pass

    @abstractmethod
    async def teardown(self) -> None:
        """Teardown the plugin. Called when the plugin is unloaded."""
        pass

    def get_info(self) -> dict[str, Any]:
        """Get plugin information."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "enabled": self.enabled,
        }

    async def enable(self) -> None:
        """Enable the plugin."""
        self.enabled = True

    async def disable(self) -> None:
        """Disable the plugin."""
        self.enabled = False

import discord
from discord.ext import commands

from epicbot.plugins.base import BasePlugin


class Plugin(BasePlugin):
    """Plugin manager commands for loading, unloading, and managing plugins."""

    def __init__(self, bot):
        super().__init__(bot)
        self.name = "Plugin Manager"
        self.version = "1.0.0"
        self.description = "Commands for managing bot plugins"
        self.author = "EpicBot Team"

    async def setup(self) -> None:
        """Setup the plugin manager commands."""
        await self.bot.add_cog(PluginManagerCommands(self.bot))

    async def teardown(self) -> None:
        """Teardown the plugin manager commands."""
        await self.bot.remove_cog("PluginManagerCommands")


class PluginManagerCommands(commands.Cog):
    """Commands for managing plugins."""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="plugins")
    @commands.is_owner()
    async def list_plugins(self, ctx: commands.Context) -> None:
        """List all loaded plugins. (Bot owner only)"""
        loaded_plugins = self.bot.plugin_manager.get_loaded_plugins()

        if not loaded_plugins:
            embed = discord.Embed(
                title="📦 Loaded Plugins",
                description="No plugins are currently loaded.",
                color=discord.Color.orange(),
            )
        else:
            embed = discord.Embed(
                title="📦 Loaded Plugins",
                description=f"Currently loaded: {len(loaded_plugins)} plugins",
                color=discord.Color.green(),
            )

            for plugin_name in loaded_plugins:
                plugin = self.bot.plugin_manager.get_plugin(plugin_name)
                if plugin:
                    info = plugin.get_info()
                    status = "✅ Enabled" if info["enabled"] else "❌ Disabled"
                    embed.add_field(
                        name=f"{info['name']} v{info['version']}",
                        value=f"{info['description']}\nStatus: {status}",
                        inline=False,
                    )

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="load_plugin")
    @commands.is_owner()
    async def load_plugin(self, ctx: commands.Context, plugin_name: str) -> None:
        """Load a plugin by name. (Bot owner only)"""
        success = await self.bot.plugin_manager.load_plugin(plugin_name)

        if success:
            embed = discord.Embed(
                title="✅ Plugin Loaded",
                description=f"Successfully loaded plugin: {plugin_name}",
                color=discord.Color.green(),
            )
        else:
            embed = discord.Embed(
                title="❌ Plugin Load Failed",
                description=f"Failed to load plugin: {plugin_name}",
                color=discord.Color.red(),
            )

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="unload_plugin")
    @commands.is_owner()
    async def unload_plugin(self, ctx: commands.Context, plugin_name: str) -> None:
        """Unload a plugin by name. (Bot owner only)"""
        if plugin_name in ["core_commands", "plugin_manager_commands"]:
            embed = discord.Embed(
                title="❌ Cannot Unload",
                description="Core plugins cannot be unloaded.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        success = await self.bot.plugin_manager.unload_plugin(plugin_name)

        if success:
            embed = discord.Embed(
                title="✅ Plugin Unloaded",
                description=f"Successfully unloaded plugin: {plugin_name}",
                color=discord.Color.green(),
            )
        else:
            embed = discord.Embed(
                title="❌ Plugin Unload Failed",
                description=f"Failed to unload plugin: {plugin_name}",
                color=discord.Color.red(),
            )

        await ctx.send(embed=embed)

    @commands.hybrid_command(name="reload_plugin")
    @commands.is_owner()
    async def reload_plugin(self, ctx: commands.Context, plugin_name: str) -> None:
        """Reload a plugin by name. (Bot owner only)"""
        success = await self.bot.plugin_manager.reload_plugin(plugin_name)

        if success:
            embed = discord.Embed(
                title="✅ Plugin Reloaded",
                description=f"Successfully reloaded plugin: {plugin_name}",
                color=discord.Color.green(),
            )
        else:
            embed = discord.Embed(
                title="❌ Plugin Reload Failed",
                description=f"Failed to reload plugin: {plugin_name}",
                color=discord.Color.red(),
            )

        await ctx.send(embed=embed)

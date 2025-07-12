from epicbot.database.connection import DatabaseManager


class GuildManager:
    """Manages guild settings and prefixes in the database."""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    async def ensure_guild_exists(self, guild_id: int, guild_name: str) -> None:
        """Ensure guild exists in database, create if it doesn't."""
        await self.db.execute(
            """
            INSERT INTO guilds (id, name, created_at, updated_at)
            VALUES ($1, $2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                updated_at = CURRENT_TIMESTAMP
            """,
            guild_id,
            guild_name,
        )

    async def get_guild_prefixes(self, guild_id: int) -> list[str]:
        """Get all prefixes for a guild."""
        rows = await self.db.fetch(
            "SELECT prefix FROM guild_prefixes WHERE guild_id = $1 ORDER BY prefix",
            guild_id,
        )
        return [row["prefix"] for row in rows]

    async def add_guild_prefix(self, guild_id: int, prefix: str) -> bool:
        """Add a prefix to a guild. Returns True if added, False if already exists."""
        try:
            await self.db.execute(
                """
                INSERT INTO guild_prefixes (guild_id, prefix, created_at)
                VALUES ($1, $2, CURRENT_TIMESTAMP)
                """,
                guild_id,
                prefix,
            )
            return True
        except Exception:
            # Prefix already exists (PRIMARY KEY constraint)
            return False

    async def remove_guild_prefix(self, guild_id: int, prefix: str) -> bool:
        """Remove a specific prefix from a guild. Returns True if removed, False if not found."""
        result = await self.db.execute(
            "DELETE FROM guild_prefixes WHERE guild_id = $1 AND prefix = $2",
            guild_id,
            prefix,
        )
        # Check if any rows were affected
        return "DELETE 1" in result

    async def clear_guild_prefixes(self, guild_id: int) -> int:
        """Remove all prefixes from a guild. Returns number of prefixes removed."""
        result = await self.db.execute(
            "DELETE FROM guild_prefixes WHERE guild_id = $1", guild_id
        )
        # Extract number from result like "DELETE 3"
        if "DELETE" in result:
            return int(result.split()[1])
        return 0

    async def get_prefix_count(self, guild_id: int) -> int:
        """Get the number of prefixes for a guild."""
        count = await self.db.fetchval(
            "SELECT COUNT(*) FROM guild_prefixes WHERE guild_id = $1", guild_id
        )
        return count or 0

    async def is_default_prefix_enabled(self, guild_id: int) -> bool:
        """Check if the default prefix '!' is enabled for a guild."""
        enabled = await self.db.fetchval(
            "SELECT default_prefix_enabled FROM guilds WHERE id = $1", guild_id
        )
        return enabled if enabled is not None else True

    async def set_default_prefix_enabled(self, guild_id: int, enabled: bool) -> None:
        """Enable or disable the default prefix '!' for a guild."""
        await self.db.execute(
            """
            INSERT INTO guilds (id, name, default_prefix_enabled, created_at, updated_at)
            VALUES ($1, 'Unknown', $2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ON CONFLICT (id) DO UPDATE SET
                default_prefix_enabled = EXCLUDED.default_prefix_enabled,
                updated_at = CURRENT_TIMESTAMP
            """,
            guild_id,
            enabled,
        )

import logging
from typing import Any

import asyncpg

from epicbot.core.config import Config


class DatabaseManager:
    """Manages database connections and operations."""

    def __init__(self, config: Config | None = None):
        self.config = config or Config()
        self.logger = logging.getLogger(__name__)
        self.pool: asyncpg.Pool | None = None

    async def initialize(self) -> None:
        """Initialize database connection pool."""
        try:
            self.pool = await asyncpg.create_pool(
                self.config.database_url,
                min_size=self.config.database_pool_min_size,
                max_size=self.config.database_pool_max_size,
            )

            self.logger.info("Database connection pool created successfully")
            await self._create_tables()

        except Exception as error:
            self.logger.error(f"Failed to initialize database: {error}")
            raise

    async def close(self) -> None:
        """Close database connection pool."""
        if self.pool:
            await self.pool.close()
            self.logger.info("Database connection pool closed")

    async def _create_tables(self) -> None:
        """Create necessary database tables."""
        if self.pool is None:
            raise RuntimeError("Database pool not initialized")
        async with self.pool.acquire() as connection:
            await connection.execute("""
                CREATE TABLE IF NOT EXISTS guilds (
                    id BIGINT PRIMARY KEY,
                    name TEXT NOT NULL,
                    prefix TEXT DEFAULT '!',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            await connection.execute("""
                CREATE TABLE IF NOT EXISTS guild_plugins (
                    guild_id BIGINT REFERENCES guilds(id) ON DELETE CASCADE,
                    plugin_name TEXT NOT NULL,
                    enabled BOOLEAN DEFAULT TRUE,
                    config JSONB DEFAULT '{}',
                    installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (guild_id, plugin_name)
                )
            """)

            await connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id BIGINT PRIMARY KEY,
                    username TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.logger.info("Database tables created/verified successfully")

    async def execute(self, query: str, *args: Any) -> str:
        """Execute a query and return the result."""
        if self.pool is None:
            raise RuntimeError("Database pool not initialized")
        async with self.pool.acquire() as connection:
            return str(await connection.execute(query, *args))

    async def fetch(self, query: str, *args: Any) -> Any:
        """Fetch multiple rows from a query."""
        if self.pool is None:
            raise RuntimeError("Database pool not initialized")
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query: str, *args: Any) -> Any:
        """Fetch a single row from a query."""
        if self.pool is None:
            raise RuntimeError("Database pool not initialized")
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def fetchval(self, query: str, *args: Any) -> Any:
        """Fetch a single value from a query."""
        if self.pool is None:
            raise RuntimeError("Database pool not initialized")
        async with self.pool.acquire() as connection:
            return await connection.fetchval(query, *args)

import logging
from typing import Any

import asyncpg

from epicbot.core.config import Config
from epicbot.database.migrator import DatabaseMigrator


class DatabaseManager:
    """Manages database connections and operations."""

    def __init__(self, config: Config | None = None):
        self.config = config or Config()
        self.logger = logging.getLogger(__name__)
        self.pool: asyncpg.Pool | None = None
        self.migrator = DatabaseMigrator(self.config)

    async def initialize(self) -> None:
        """Initialize database connection pool."""
        try:
            self.pool = await asyncpg.create_pool(
                self.config.database_url,
                min_size=self.config.database_pool_min_size,
                max_size=self.config.database_pool_max_size,
            )

            self.logger.info("Database connection pool created successfully")
            await self._run_migrations()

        except Exception as error:
            self.logger.error(f"Failed to initialize database: {error}")
            raise

    async def close(self) -> None:
        """Close database connection pool."""
        if self.pool:
            await self.pool.close()
            self.logger.info("Database connection pool closed")

    async def _run_migrations(self) -> None:
        """Run database migrations."""
        self.logger.info("Running database migrations...")
        success = await self.migrator.run_migrations()
        if not success:
            raise RuntimeError("Database migrations failed")
        self.logger.info("Database migrations completed successfully")

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

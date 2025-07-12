import logging
from pathlib import Path

import asyncpg

from epicbot.core.config import Config


class DatabaseMigrator:
    """Handles database migrations for EpicBot."""

    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.migrations_dir = Path(__file__).parent / "migrations"

    async def get_applied_migrations(self, connection: asyncpg.Connection) -> list[int]:
        """Get list of already applied migration versions."""
        try:
            # First check if migrations table exists
            table_exists = await connection.fetchval("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = 'schema_migrations'
                )
            """)

            if not table_exists:
                return []

            rows = await connection.fetch(
                "SELECT version FROM schema_migrations ORDER BY version"
            )
            return [row["version"] for row in rows]
        except Exception as e:
            self.logger.error(f"Error getting applied migrations: {e}")
            return []

    def get_available_migrations(self) -> list[tuple[int, str, Path]]:
        """Get list of available migration files."""
        migrations = []

        if not self.migrations_dir.exists():
            self.logger.warning(
                f"Migrations directory not found: {self.migrations_dir}"
            )
            return migrations

        for migration_file in sorted(self.migrations_dir.glob("*.sql")):
            try:
                # Extract version from filename like "001_initial_schema.sql"
                filename = migration_file.stem
                version_str = filename.split("_")[0]
                version = int(version_str)
                name = "_".join(filename.split("_")[1:])
                migrations.append((version, name, migration_file))
            except (ValueError, IndexError) as e:
                self.logger.warning(
                    f"Invalid migration filename format: {migration_file.name}: {e}"
                )
                continue

        return migrations

    async def apply_migration(
        self, connection: asyncpg.Connection, version: int, name: str, file_path: Path
    ) -> bool:
        """Apply a single migration."""
        try:
            self.logger.info(f"Applying migration {version}: {name}")

            # Read and execute migration SQL
            sql_content = file_path.read_text(encoding="utf-8")
            await connection.execute(sql_content)

            self.logger.info(f"Successfully applied migration {version}: {name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to apply migration {version}: {name}: {e}")
            return False

    async def run_migrations(self) -> bool:
        """Run all pending migrations."""
        try:
            # Create connection
            connection = await asyncpg.connect(self.config.database_url)

            try:
                # Get applied and available migrations
                applied_migrations = await self.get_applied_migrations(connection)
                available_migrations = self.get_available_migrations()

                if not available_migrations:
                    self.logger.info("No migration files found")
                    return True

                # Find pending migrations
                pending_migrations = [
                    (version, name, file_path)
                    for version, name, file_path in available_migrations
                    if version not in applied_migrations
                ]

                if not pending_migrations:
                    self.logger.info("All migrations are up to date")
                    return True

                self.logger.info(
                    f"Found {len(pending_migrations)} pending migration(s)"
                )

                # Apply each pending migration in a transaction
                async with connection.transaction():
                    for version, name, file_path in pending_migrations:
                        success = await self.apply_migration(
                            connection, version, name, file_path
                        )
                        if not success:
                            return False

                self.logger.info("All migrations applied successfully")
                return True

            finally:
                await connection.close()

        except Exception as e:
            self.logger.error(f"Error running migrations: {e}")
            return False

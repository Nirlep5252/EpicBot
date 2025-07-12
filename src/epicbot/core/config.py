from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Application configuration settings."""

    discord_token: str
    database_url: str
    debug: bool = False

    # Plugin system settings
    plugins_directory: str = "src/epicbot/plugins"
    max_plugins_per_guild: int = 50

    # Database settings
    database_pool_min_size: int = 5
    database_pool_max_size: int = 20

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        if not self.discord_token:
            raise ValueError("DISCORD_TOKEN environment variable is required")

        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is required")

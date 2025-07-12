import os
from unittest.mock import patch

import pytest

from epicbot.core.config import Config


def test_config_requires_discord_token():
    """Test that Config raises ValueError when DISCORD_TOKEN is missing."""
    with (
        patch.dict(os.environ, {}, clear=True),
        pytest.raises(
            ValueError, match="DISCORD_TOKEN environment variable is required"
        ),
    ):
        Config()


def test_config_requires_database_url():
    """Test that Config raises ValueError when DATABASE_URL is missing."""
    with (
        patch.dict(os.environ, {"DISCORD_TOKEN": "test_token"}, clear=True),
        pytest.raises(
            ValueError, match="DATABASE_URL environment variable is required"
        ),
    ):
        Config()


def test_config_with_valid_values():
    """Test that Config initializes correctly with valid environment variables."""
    with patch.dict(
        os.environ,
        {
            "DISCORD_TOKEN": "test_token",
            "DATABASE_URL": "postgresql://test:test@localhost:5432/test",
        },
        clear=True,
    ):
        config = Config()
        assert config.discord_token == "test_token"
        assert config.database_url == "postgresql://test:test@localhost:5432/test"
        assert config.debug is False  # default value
        assert config.max_plugins_per_guild == 50  # default value

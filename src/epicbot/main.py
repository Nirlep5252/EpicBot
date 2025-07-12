import asyncio
import logging
import signal
import sys

from dotenv import load_dotenv

from epicbot.core.bot import EpicBot
from epicbot.core.config import Config
from epicbot.database.connection import DatabaseManager




async def main() -> None:
    """Main entry point for EpicBot."""
    load_dotenv()

    config = Config()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger(__name__)
    logger.info("Starting EpicBot...")

    bot = None
    db_manager = None

    def signal_handler(sig, frame):
        """Handle shutdown signals gracefully."""
        logger.info("Received shutdown signal, cleaning up...")
        sys.exit(0)

    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        db_manager = DatabaseManager()
        await db_manager.initialize()

        bot = EpicBot(config=config)
        await bot.start(config.discord_token)

    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down gracefully...")
    except Exception as error:
        logger.error(f"Failed to start bot: {error}")
        raise
    finally:
        # Cleanup resources
        if bot:
            logger.info("Closing bot connection...")
            await bot.close()

        if db_manager and db_manager.pool:
            logger.info("Closing database connection...")
            await db_manager.close()

        logger.info("Shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())

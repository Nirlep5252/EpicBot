import logging
import asyncio
import logging.handlers
import os
import discord
import asyncpg

from dotenv import load_dotenv
from discord.ext import commands
from aiohttp import ClientSession
from bot import EpicBot

load_dotenv()


async def main():
    TOKEN = os.getenv("BETA_TOKEN")
    if not TOKEN:
        raise ValueError("No token provided")

    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "[{asctime}] [{levelname:<8}] {name}: {message}",
            "%Y-%m-%d %H:%M:%S",
            style="{",
        )
    )
    logger.addHandler(handler)

    async with ClientSession() as client, asyncpg.create_pool(
        user="postgres", command_timeout=30
    ) as pool:
        intents = discord.Intents.default()
        async with EpicBot(
            commands.when_mentioned,
            db_pool=pool,
            web_client=client,
            intents=intents,
            initial_extensions=["extensions.hello"],
        ) as bot:
            await bot.start(TOKEN)


asyncio.run(main())

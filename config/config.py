from dataclasses import dataclass
from environs import Env
from os import environ
from pathlib import Path
from typing import Optional


@dataclass
class TgBot:
    token: str  # Token for accessing the Telegram bot


@dataclass
class RedisStorage:
    """
    Configuration for Redis storage.
    """

    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None


@dataclass
class Config:
    """
    Configuration class for the application.
    Contains settings for the Telegram bot and Redis storage.
    """

    tg_bot: TgBot
    redis: RedisStorage
    # paths: Paths Reserved for future use, currently not implemented


def load_config(path: Optional[Path] = None) -> Config:
    """
    Load configuration from environment variables.
    If a path is provided, it reads from the specified .env file.

    Args:
        path Optional[str]: Path to the .env file. If None, defaults to the current directory.

    Returns:
        Config: An instance of the Config class populated with the environment variables.
    """
    env: Env = Env()
    env.read_env(path)

    environ["LOG_FILE"] = env.str("LOG_FILE")
    environ["PROCESSED_MACS"] = env.str("PROCESSED_MACS")
    environ["FRESH_LIMIT_MINUTES"] = env.str("FRESH_LIMIT_MINUTES")
    environ["NAME_TEMPLATE"] = env.str("NAME_TEMPLATE")

    return Config(
        tg_bot=TgBot(token=env.str("BOT_TOKEN")),
        redis=RedisStorage(
            host=env.str("REDIS_HOST", default="localhost"),
            port=env.int("REDIS_PORT", default=6379),
            db=env.int("REDIS_DB", default=0),
            password=env.str("REDIS_PASSWORD", default=None),
        ),
    )

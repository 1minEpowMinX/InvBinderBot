from dataclasses import dataclass
from environs import Env
from pathlib import Path
from typing import Optional
from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage


@dataclass
class TgBot:
    """
    Configuration for the Telegram bot.
    """

    token: str


@dataclass
class RedisConfig:
    """
    Configuration for Redis.
    """

    host: str
    port: int
    db: int
    password: Optional[str] = None

    def create_client(self) -> Redis:
        """
        Create and return a Redis client instance.
        """
        return Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
        )

    def create_storage(self) -> RedisStorage:
        """
        Create and return a RedisStorage instance.
        """
        return RedisStorage(self.create_client())


@dataclass
class FilesConfig:
    """
    Configuration for files.
    """

    log_file: Path
    processed_macs: Path
    fresh_limit: float
    name_template: str


@dataclass
class Config:
    """
    Configuration for the bot.
    """

    tg_bot: TgBot
    redis: RedisConfig
    files: FilesConfig


def load_config(path: Optional[Path] = None) -> Config:
    """
    Load configuration from .env file or environment variables.

    Args:
        path (Optional[Path]): Path to the .env file. Defaults to None, which uses the current directory.

    Returns:
        Config: The loaded configuration object.
    """

    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(token=env.str("BOT_TOKEN")),
        redis=RedisConfig(
            host=env.str("REDIS_HOST", "localhost"),
            port=env.int("REDIS_PORT", 6379),
            db=env.int("REDIS_DB", 0),
            password=env.str("REDIS_PASSWORD", None),
        ),
        files=FilesConfig(
            log_file=Path(env.str("LOG_FILE", "dhcp.log")),
            processed_macs=Path(env.str("PROCESSED_MACS", "processed_macs.csv")),
            fresh_limit=float(env.str("FRESH_LIMIT_MINUTES", "5")),
            name_template=env.str("NAME_TEMPLATE", "{}"),
        ),
    )

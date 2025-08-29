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

    Attributes:
        token (str): The bot token provided by BotFather.
    """

    token: str


@dataclass
class RedisConfig:
    """
    Configuration for Redis to create a Redis client and a RedisStorage for FSM.

    Attributes:
        host (str): Redis server host.
        port (int): Redis server port.
        db (int): Redis database index.
        password (Optional[str]): Redis server password.
    """

    host: str
    port: int
    db: int
    password: Optional[str] = None

    def create_client(self) -> Redis:
        """
        Create and return a Redis client instance using the provided configuration.

        Returns:
            Redis: An instance of the Redis client.
        """

        return Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
        )

    def create_storage(self) -> RedisStorage:
        """
        Create and return a RedisStorage instance for FSM.

        Returns:
            RedisStorage: An instance of RedisStorage.
        """

        return RedisStorage(self.create_client())


@dataclass
class FilesConfig:
    """
    Configuration for file paths and related settings.

    Attributes:
        log_file (Path): Path to the log file.
        processed_macs (Path): Path to the processed MAC addresses file.
        fresh_limit (float): Time limit in minutes to consider a MAC address as fresh.
        name_template (str): Template for naming entries, with a placeholder for dynamic content.
    """

    log_file: Path
    processed_macs: Path
    fresh_limit: float
    name_template: str


@dataclass
class Config:
    """
    Main configuration class that aggregates all other configurations.

    Attributes:
        tg_bot (TgBot): Configuration for the Telegram bot.
        redis (RedisConfig): Configuration for Redis.
        files (FilesConfig): Configuration for file paths and related settings.
    """

    tg_bot: TgBot
    redis: RedisConfig
    files: FilesConfig


def load_config(path: Optional[Path] = None) -> Config:
    """
    Load configuration from environment variables or a .env file.

    Args:
        path (Optional[Path]): Path to the .env file. Defaults to None, which uses the current directory.

    Returns:
        Config: The loaded configuration object. Includes bot, Redis, and file configurations.
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

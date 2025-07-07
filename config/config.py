from dataclasses import dataclass
from environs import Env
from typing import Optional


@dataclass
class TgBot:
    token: str  # Token for accessing the Telegram bot


# @dataclass
# class Paths:
#     log_file: str
#     processed_macs: str
#     new_macs: str


@dataclass
class Config:
    """
    Configuration class for the application.
    Contains settings for the Telegram bot.
    """

    tg_bot: TgBot
    # paths: Paths Reserved for future use, currently not implemented


def load_config(path: Optional[str] = None) -> Config:
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

    return Config(tg_bot=TgBot(token=env.str("BOT_TOKEN")))

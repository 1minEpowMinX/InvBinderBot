from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from logging import Logger
from typing import Any, Awaitable, Callable, Dict


class LoggingMiddleware(BaseMiddleware):
    """
    Middleware for logging incoming messages and callback queries in a Telegram bot.

    This middleware logs the user who sent the message or callback query,
    along with the content of the message or callback data.

    Attributes:
        logger (Logger): An instance of Logger to log messages.
    """

    def __init__(self, logger: Logger):
        self.logger = logger

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = data["event_from_user"]
        callback_data = getattr(event, "data", "")
        if callback_data:
            text = f"Callback data: {callback_data}"
        else:
            text = getattr(event, "text", "No text available")
        self.logger.info(f"Incoming message from {user.full_name} ({user.id}): {text}")

        # Add the logger to the data context for further use in handlers
        data["logger"] = self.logger

        # Call the next handler in the middleware chain
        return await handler(event, data)

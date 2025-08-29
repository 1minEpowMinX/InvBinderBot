from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from logging import Logger
from typing import Any, Awaitable, Callable, Dict


class LoggingMiddleware(BaseMiddleware):
    """
    Middleware for logging incoming messages.

    This middleware logs the user's full name, user ID, and the text of the incoming message.
    It also adds the logger to the request context for further use in handlers.

    Attributes:
        logger (Logger): An instance of Logger for logging messages.
    """

    def __init__(self, logger: Logger) -> None:
        """
        Initialize the LoggingMiddleware with a Logger instance.

        Args:
            logger (Logger): An instance of Logger for logging messages.
        """

        self.logger = logger

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        Middleware call method.

        This method logs the user's full name, user ID, and the text of the incoming message.
        It also adds the logger to the request context for further use in handlers.

        Args:
            handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]): The next handler in the middleware chain.
            event (TelegramObject): The incoming Telegram event.
            data (Dict[str, Any]): The data context for the request.

        Returns:
            Any: The result of the next handler in the middleware chain.
        """

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

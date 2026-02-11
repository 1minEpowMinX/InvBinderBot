from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Awaitable, Dict, Any

from keyboards.reply import get_menu_by_role
from utils.auth_manager import AuthManager


class AuthMiddleware(BaseMiddleware):
    """
    Middleware for handling user authorization and role management.

    This middleware checks the user's role and adds relevant data to the request context.
    It also provides a keyboard based on the user's role.

    Attributes:
        auth (AuthManager): An instance of AuthManager for managing user roles and permissions.
    """

    def __init__(self, auth: AuthManager) -> None:
        """
        Initialize the AuthMiddleware with an AuthManager instance.

        Args:
            auth (AuthManager): An instance of AuthManager for managing user roles and permissions.
        """
        self.auth = auth

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        Middleware call method.

        This method checks the user's role and adds relevant data to the request context.
        It also provides a keyboard based on the user's role.

        Args:
            handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]): The next handler in the middleware chain.
            event (TelegramObject): The incoming Telegram event.
            data (Dict[str, Any]): The data context for the request.

        Returns:
            Any: The result of the next handler in the middleware chain.
        """
        user = data["event_from_user"]
        role = await self.auth.get_role(user.id)

        data["logger"].info(f"User {user.full_name} ({user.id}) has role: {role}")

        # Add to data context everything needed for further use in handlers
        data["auth"] = self.auth
        data["role"] = role
        data["keyboard"] = get_menu_by_role(role)

        # Call the next handler in the middleware chain
        return await handler(event, data)

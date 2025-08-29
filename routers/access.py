from aiogram import Router, F
from aiogram.types import Message
from logging import Logger

from keyboards.access import access_request_markup
from lexicon.lexicon import get_message, get_menu_button
from utils.auth_manager import AuthManager

router = Router()


@router.message(F.text == get_menu_button("request_access"))  # type: ignore
async def request_access_handler(
    message: Message, auth: AuthManager, logger: Logger, bot
) -> None:
    """
    Handles the request for access to the bot by a user.

    This function retrieves the user information from the message,
    checks for available admins, and sends a request message to them.

    Args:
        message (Message): The incoming message that triggered the request.
        auth (AuthManager): The authorization manager instance to handle user roles.
        logger (Logger): The logger instance for logging events.
        bot: The bot instance to send messages.
    """

    user = message.from_user  # type: ignore
    user_id = user.id  # type: ignore
    full_name = user.full_name  # type: ignore

    logger.info(f"User {full_name} ({user_id}) requested access to the bot.")

    admin_ids = [
        uid for uid in auth.get_list_users().keys() if auth.get_role(uid) == "admin"
    ]

    if not admin_ids:
        logger.warning(
            f"User {user_id} ({full_name}) attempted to request access, but no admins found."
        )
        await message.answer(get_message("no_admins"))
        return

    markup = access_request_markup(user_id)

    for admin_id in admin_ids:
        await bot.send_message(
            chat_id=admin_id,
            text=get_message("request_access_from_user").format(
                full_name=full_name, user_id=user_id
            ),
            parse_mode="HTML",
            reply_markup=markup,
        )

    await message.answer(get_message("request_access_sent"))

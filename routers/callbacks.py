from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram import Bot
from logging import Logger

from keyboards.reply import get_menu_by_role
from lexicon.lexicon import get_message
from utils.auth_manager import AuthManager

router = Router()


@router.callback_query(F.data.startswith("approve:"))
async def approve_user_callback(
    callback: CallbackQuery, role: str, auth: AuthManager, bot: Bot, logger: Logger
):
    """
    Handles the callback for approving a user request.

    This function checks if the user has admin rights, retrieves the user ID from the callback data,
    and adds the user to the authorization system.

    Args:
        callback (CallbackQuery): The callback query object containing user interaction data.
        role (str): The role of the user (should be 'admin' for this command).
        bot (Bot): The bot instance to send messages.
        logger (Logger): The logger instance for logging events.
    """
    admin_id = callback.from_user.id
    data = callback.data.split(":")  # type: ignore
    user_id = int(data[1])  # Retrieve user ID from callback data

    if role != "admin":
        logger.warning(
            f"User {callback.from_user.id} ({callback.from_user.full_name}) attempted to approve user without permission."  # type: ignore
        )
        await callback.answer(get_message("no_access"), show_alert=True)
        return

    # Retrieve user's data from get_chat method
    try:
        user_chat = await bot.get_chat(user_id)
        full_name = user_chat.full_name
    except:
        full_name = get_message("unknown_user")  # Fallback if user not found

    # Add user and check if the user already exists in the auth system
    if auth.add_user(
        user_id,
        added_by=admin_id,
        full_name=full_name,
        role="user",
        notes=get_message("note").format(
            admin_username=callback.from_user.full_name, admin_id=admin_id
        ),
    ):
        await bot.edit_message_text(
            text=get_message("add_user").format(full_name=full_name, user_id=user_id),
            chat_id=callback.message.chat.id,  # type: ignore
            message_id=callback.message.message_id,  # type: ignore
            parse_mode="HTML",
        )
        await bot.send_message(
            chat_id=user_id,
            text=get_message("approve_access"),
            reply_markup=get_menu_by_role("user"),
        )
    else:
        await callback.answer(
            get_message("user_already_exists").format(user_id=user_id), show_alert=True
        )


@router.callback_query(F.data.startswith("deny:"))
async def deny_user_callback(callback: CallbackQuery, bot: Bot):
    """
    Handles the callback for denying a user request.

    This function retrieves the user ID from the callback data and sends a denial message to the user.

    Args:
        callback (CallbackQuery): The callback query object containing user interaction data.
        bot (Bot): The bot instance to send messages.
    """
    user_id = int(callback.data.split(":")[1])  # type: ignore
    await bot.edit_message_text(
        text=get_message("admin_request_denied"),
        chat_id=callback.message.chat.id,  # type: ignore
        message_id=callback.message.message_id,  # type: ignore
    )
    await bot.send_message(
        chat_id=user_id,
        text=get_message("user_request_denied"),
    )


@router.callback_query(F.data.startswith("delete:"))
async def delete_user_callback(
    callback: CallbackQuery, auth: AuthManager, logger: Logger, bot: Bot
):
    """
    Handles the callback for deleting a user.

    This function checks if the user has admin rights, retrieves the user ID from the callback data,
    and removes the user from the authorization system.

    Args:
        callback (CallbackQuery): The callback query object containing user interaction data.
        bot (Bot): The bot instance to send messages.
        auth (AuthManager): The authorization manager instance to handle user roles.
        logger (Logger): The logger instance for logging events.
    """
    admin_id = callback.from_user.id
    if not auth.is_admin(admin_id):
        logger.warning(
            f"User {callback.from_user.id} ({callback.from_user.full_name}) attempted to delete user without permission."  # type: ignore
        )
        await callback.answer(get_message("no_access"), show_alert=True)
        return

    user_id = int(callback.data.split(":")[1])  # type: ignore

    # Check if the admin is trying to delete themselves and if they are the only admin
    if (
        user_id == admin_id
        and sum(
            1 for uid in auth.get_list_users().keys() if auth.get_role(uid) == "admin"
        )
        == 1
    ):
        await callback.answer(
            get_message("only_admin"),
            show_alert=True,
        )
        return

    if auth.remove_user(user_id):
        await bot.edit_message_text(
            text=get_message("user_deleted").format(user_id=user_id),
            chat_id=callback.message.chat.id,  # type: ignore
            message_id=callback.message.message_id,  # type: ignore
        )
        logger.info(
            f"Admin {callback.from_user.full_name} ({admin_id}) deleted user {user_id}"
        )
    else:
        await callback.answer(
            get_message("user_not_found").format(user_id=user_id), show_alert=True
        )

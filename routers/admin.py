from aiogram import Router, F
from aiogram.filters import Command, CommandObject, or_f
from aiogram.types import Message
from logging import Logger

from keyboards.delete import delete_user_markup
from lexicon.lexicon import get_message, get_menu_button
from services.command import assign_role_commands
from utils.auth_manager import AuthManager
from utils.formatting import format_user_entry

router = Router()


@router.message(F.text == get_menu_button("delete_user"))  # type: ignore
async def delete_user_prompt(
    message: Message, role: str, auth: AuthManager, logger: Logger
):
    """
    Prompts the admin to delete a user.
    This function lists all users and provides an option to delete them.

    Args:
        message (Message): The incoming message that triggered the command.
        auth (AuthManager): The authorization manager instance to handle user roles.
        role (str): The role of the user (should be 'admin' for this command).
        logger (Logger): The logger instance for logging events.
    """
    if role != "admin":
        logger.warning(
            f"User {message.from_user.id} ({message.from_user.full_name}) attempted to access delete user without permission."  # type: ignore
        )
        await message.answer(get_message("no_access"))
        return

    users = auth.get_list_users()
    if not users:
        await message.answer(get_message("empty_users"))
        return

    for i, (uid, user) in enumerate(users.items(), start=1):
        await message.answer(
            text=format_user_entry(uid, user, i),
            parse_mode="HTML",
            reply_markup=delete_user_markup(uid),
        )


@router.message(Command("delete_user"))
async def delete_user_command(
    message: Message,
    command: CommandObject,
    role: str,
    auth: AuthManager,
    logger: Logger,
):
    """
    Deletes a user by their ID.
    This command is restricted to admin users only.

    Args:
        message (Message): The incoming message that triggered the command.
        command (CommandObject): The command object containing the command arguments.
        role (str): The role of the user (should be 'admin' for this command).
        auth (AuthManager): The authorization manager instance to handle user roles.
        logger (Logger): The logger instance for logging events.
    """
    if role != "admin":
        logger.warning(
            f"User {message.from_user.id} ({message.from_user.full_name}) attempted to access delete user without permission."  # type: ignore
        )
        await message.answer(get_message("no_access"))
        return

    arg = command.args
    if not arg or not arg.isdigit():
        await message.answer(
            get_message("needs_id_for_delete"),
            parse_mode="HTML",
        )
        return

    user_id = int(arg)

    if auth.remove_user(user_id):
        await message.answer(
            get_message("user_deleted").format(user_id=user_id), parse_mode="HTML"
        )
        logger.info(f"Admin {message.from_user.full_name} ({message.from_user.id}) deleted the user {user_id}")  # type: ignore
    else:
        await message.answer(
            get_message("user_not_found").format(user_id=user_id), parse_mode="HTML"
        )


@router.message(or_f(Command("user_list"), F.text == get_menu_button("user_list")))  # type: ignore
async def list_users_handler(
    message: Message, role: str, auth: AuthManager, logger: Logger
):
    """
    Lists all registered users.
    This command is restricted to admin users only.

    Args:
        message (Message): The incoming message that triggered the command.
        role (str): The role of the user (should be 'admin' for this command).
        auth (AuthManager): The authorization manager instance to handle user roles.
        logger (Logger): The logger instance for logging events.
    """
    if role != "admin":
        logger.warning(
            f"User {message.from_user.id} ({message.from_user.full_name}) attempted to access user list without permission."  # type: ignore
        )
        await message.answer(get_message("no_access"))
        return

    users = auth.get_list_users()
    if not users:
        logger.info("No registered users found.")
        await message.answer(get_message("empty_users"))
        return

    logger.info(f"Admin {message.from_user.full_name} ({message.from_user.id}) requested user list.")  # type: ignore

    result = f"<b>{get_menu_button('user_list')}:</b>\n\n" + "\n".join(  # type: ignore
        format_user_entry(uid, user, i)
        for i, (uid, user) in enumerate(users.items(), start=1)
    )

    await message.answer(result, parse_mode="HTML")


@router.message(Command("reload_users"))
async def reload_users_handler(
    message: Message, role: str, auth: AuthManager, logger: Logger
):
    """
    Reloads the list of users from the file.
    This command is restricted to admin users only.

    Args:
        message (Message): The incoming message that triggered the command.
        role (str): The role of the user (should be 'admin' for this command).
        auth (AuthManager): The authorization manager instance to handle user roles.
        logger (Logger): The logger instance for logging events.
    """
    if role != "admin":
        logger.warning(
            f"User {message.from_user.id} ({message.from_user.full_name}) attempted to access reload users without permission."  # type: ignore
        )
        await message.answer(get_message("no_access"))
        return
    auth.reload()
    await assign_role_commands(message.bot, auth)  # type: ignore
    logger.info(f"Admin {message.from_user.full_name} ({message.from_user.id}) reloaded users.")  # type: ignore

    await message.answer(get_message("users_update"))

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, or_f
from logging import Logger

from keyboards.delete import delete_user_markup
from utils.auth_manager import AuthManager
from utils.formatting import format_user_entry

router = Router()


@router.message(Command("reload_users"))
async def reload_users_handler(message: Message, role: str, auth: AuthManager):
    if role != "admin":
        await message.answer("⛔ У вас нет прав на обновление пользователей.")
        return
    auth.reload()
    await message.answer("🔄 Список пользователей обновлён из файла.")


@router.message(F.text == "🗑️ Удалить пользователя")
async def delete_user_prompt(
    message: Message, auth: AuthManager, role: str, logger: Logger
):
    if role != "admin":
        logger.warning(
            f"User {message.from_user.id} ({message.from_user.full_name}) attempted to access delete user without permission."  # type: ignore
        )
        await message.answer("⛔ У вас нет прав на удаление пользователей.")
        return

    users = auth.get_list_users()
    if not users:
        await message.answer("📭 Список пользователей пуст.")
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
    if role != "admin":
        await message.answer("⛔ У вас нет прав на удаление пользователей.")
        return

    arg = command.args
    if not arg or not arg.isdigit():
        await message.answer(
            "❗ Укажите ID пользователя: <code>/delete_user 123456789</code>",
            parse_mode="HTML",
        )
        return

    user_id = int(arg)

    if auth.remove_user(user_id):
        await message.answer(f"✅ Пользователь с ID {user_id} удалён.")
        logger.info(f"Admin {message.from_user.full_name} ({message.from_user.id}) deleted the user {user_id}")  # type: ignore
    else:
        await message.answer(f"❌ Пользователь с ID {user_id} не найден.")


@router.message(or_f(Command("user_list"), F.text == "📄 Список пользователей"))
async def list_users_handler(
    message: Message, role: str, auth: AuthManager, logger: Logger
):
    if role != "admin":
        logger.warning(
            f"User {message.from_user.id} ({message.from_user.full_name}) attempted to access user list without permission."  # type: ignore
        )
        await message.answer("⛔ У вас нет прав для просмотра списка пользователей.")
        return

    users = auth.get_list_users()
    if not users:
        logger.info("No registered users found.")
        await message.answer("📭 Нет зарегистрированных пользователей.")
        return

    logger.info(f"Admin {message.from_user.full_name} ({message.from_user.id}) requested user list.")  # type: ignore

    result = "<b>📄 Список пользователей:</b>\n\n" + "\n".join(
        format_user_entry(uid, user, i)
        for i, (uid, user) in enumerate(users.items(), start=1)
    )

    await message.answer(result, parse_mode="HTML")

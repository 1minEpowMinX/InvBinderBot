from aiogram import Router, F
from aiogram.types import Message
from logging import Logger

from utils.auth_manager import AuthManager
from utils.formatting import format_user_entry

router = Router()


@router.message(F.text == "📄 Список пользователей")
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

    result = "<b>📄 Список пользователей:</b>\n\n" + "\n".join(
        format_user_entry(uid, user, i)
        for i, (uid, user) in enumerate(users.items(), start=1)
    )

    await message.answer(result, parse_mode="HTML")

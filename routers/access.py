from aiogram import Router, F
from aiogram.types import Message
from logging import Logger

from keyboards.access import access_request_markup
from utils.auth_manager import AuthManager

router = Router()


@router.message(F.text == "🔑 Запросить доступ")
async def request_access_handler(
    message: Message, auth: AuthManager, logger: Logger, bot
):
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
        await message.answer("Не удалось найти администраторов. Попробуйте позже.")
        return

    markup = access_request_markup(user_id)

    for admin_id in admin_ids:
        await bot.send_message(
            chat_id=admin_id,
            text=f"👤 Пользователь <b>{full_name}</b> (ID: <code>{user_id}</code>) запросил доступ.",
            parse_mode="HTML",
            reply_markup=markup,
        )

    await message.answer("📩 Заявка на доступ отправлена администраторам.")

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram import Bot

from utils.auth_manager import AuthManager

router = Router()


@router.callback_query(F.data.startswith("approve:"))
async def approve_user_callback(callback: CallbackQuery, auth: AuthManager, bot: Bot):
    admin_id = callback.from_user.id
    data = callback.data.split(":")  # type: ignore
    user_id = int(data[1])  # Получаем ID пользователя из callback_data

    # Проверка прав (можно убрать, если обрабатывается только у админа)
    if not auth.is_admin(admin_id):
        await callback.answer(
            "⛔ У вас нет прав для выполнения действия", show_alert=True
        )
        return

    # Получим имя пользователя (если нужно — через get_chat)
    try:
        user_chat = await bot.get_chat(user_id)
        full_name = user_chat.full_name
    except:
        full_name = "Неизвестно"

    # Добавление пользователя
    if auth.add_user(
        user_id,
        added_by=admin_id,
        full_name=full_name,
        role="user",
        notes=f"Добавлен администратором {admin_id} ({callback.from_user.full_name})",
    ):
        await bot.edit_message_text(
            text=f"✅ Пользователь <b>{full_name}</b> (ID: <code>{user_id}</code>) был добавлен.",
            chat_id=callback.message.chat.id,  # type: ignore
            message_id=callback.message.message_id,  # type: ignore
            parse_mode="HTML",
        )
        await bot.send_message(
            chat_id=user_id,
            text="🎉 Вам предоставлен доступ к боту!",
        )
    else:
        await callback.answer("Пользователь уже есть.", show_alert=True)


@router.callback_query(F.data.startswith("deny:"))
async def deny_user_callback(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.data.split(":")[1])  # type: ignore
    await bot.edit_message_text(
        text="❌ Заявка отклонена.",
        chat_id=callback.message.chat.id,  # type: ignore
        message_id=callback.message.message_id,  # type: ignore
    )
    await bot.send_message(
        chat_id=user_id,
        text="🚫 Ваша заявка на доступ была отклонена.",
    )

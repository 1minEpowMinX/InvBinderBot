from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def delete_user_markup(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete:{user_id}")]
        ]
    )

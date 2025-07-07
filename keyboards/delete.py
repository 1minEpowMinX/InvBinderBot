from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def delete_user_markup(user_id: int) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup for deleting a user.

    Args:
        user_id (int): The ID of the user to be deleted.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete:{user_id}")]
        ]
    )

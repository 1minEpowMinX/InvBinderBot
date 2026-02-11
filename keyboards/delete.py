from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon import get_button


def delete_user_markup(user_id: int) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup for deleting a user.

    The keyboard includes a single "Delete" button with callback data
    that includes the user ID for reference.

    Args:
        user_id (int): The ID of the user to be deleted.

    Returns:
        InlineKeyboardMarkup: The inline keyboard markup with a delete button.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_button("delete"), callback_data=f"delete:{user_id}"
                )
            ]
        ]
    )

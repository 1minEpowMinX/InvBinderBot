from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from lexicon.lexicon import get_button


def access_request_markup(user_id: int) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup for access request approval or denial.

    Args:
        user_id (int): The ID of the user requesting access.

    Returns:
        InlineKeyboardMarkup: The inline keyboard markup with approval and denial buttons.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=get_button("approve"), callback_data=f"approve:{user_id}"
                ),
                InlineKeyboardButton(
                    text=get_button("deny"), callback_data=f"deny:{user_id}"
                ),
            ]
        ]
    )

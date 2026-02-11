from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from lexicon.lexicon import get_button


def access_request_markup(user_id: int) -> InlineKeyboardMarkup:
    """
    Creates an inline keyboard markup for access request approval or denial.

    The keyboard includes two buttons: "Approve" and "Deny", each with a callback data
    that includes the user ID for reference.

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

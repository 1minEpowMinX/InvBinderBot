from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from lexicon.lexicon import MENU_TEMPLATE, BUTTONS


def get_menu_by_role(role: str) -> ReplyKeyboardMarkup:
    """
    Returns a keyboard markup based on the user's role.

    The keyboard layout is determined by the role provided, using predefined
    templates and button labels.

    Args:
        role (str): User role (e.g., "admin", "user", "viewer").

    Returns:
        ReplyKeyboardMarkup: Keyboard markup for the specified role.
    """

    role_layout = MENU_TEMPLATE.get(role, [])
    button_labels = BUTTONS["buttons"]

    keyboard = []
    for row in role_layout:
        keyboard.append(
            [
                KeyboardButton(
                    text=button_labels.get(btn_key, f"[{btn_key}]")  # type: ignore
                )  # fallback if btn_key not in button_labels
                for btn_key in row
            ]
        )

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )

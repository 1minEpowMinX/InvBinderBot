from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_one_time_keyboard(keyboard_text: list[str]) -> ReplyKeyboardMarkup:
    """
    Creates a one-time keyboard markup with the provided text.

    The keyboard will be resized to fit the buttons and will disappear after one use.

    Args:
        keyboard_text (list[str]): A list of strings to be used as button texts in the keyboard.

    Raises:
        ValueError: If keyboard_text is empty.

    Returns:
        ReplyKeyboardMarkup: The one-time keyboard markup with the specified buttons.
    """

    if not keyboard_text:
        raise ValueError("keyboard_text must not be empty")

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=btn)] for btn in keyboard_text],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

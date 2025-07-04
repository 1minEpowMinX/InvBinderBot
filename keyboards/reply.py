from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Template: role → list of button rows (row = list of buttons)
MENU_TEMPLATE = {
    "admin": [
        ["📥 Добавить MAC", "📤 Показать новые MAC"],
        ["🧑‍💼 Добавить пользователя", "🗑 Удалить пользователя"],
        ["📄 Список пользователей"],
    ],
    "user": [
        ["📥 Добавить MAC", "📤 Показать новые MAC"],
        ["📄 Список пользователей"],
    ],
    "viewer": [
        ["🔑 Запросить доступ"],
    ],
}


def get_menu_by_role(role: str) -> ReplyKeyboardMarkup:
    """
    Returns a keyboard markup based on the user's role.

    Args:
        role (str): User role (e.g., "admin", "user", "readonly").

    Returns:
        ReplyKeyboardMarkup: Keyboard markup for the specified role.
    """
    keyboard_rows = MENU_TEMPLATE.get(role, [])
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=btn) for btn in row] for row in keyboard_rows],
        resize_keyboard=True,
    )

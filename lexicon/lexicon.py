MESSAGES = {
    "admin": """
👋 <b>Добро пожаловать, Администратор!</b>

С этим ботом вы можете:
🔎 Просматривать новые MAC-адреса  
🔗 Привязывать MAC к инвентарным номерам
👥 Управлять пользователями  
🤖 Управлять логикой бота

Нажмите <b>/help</b> для получения справки по командам.

Выберите команду или воспользуйтесь меню ниже 👇
	""",
    "admin_help": """
<b>📘 Справка по командам:</b>

🔹 <b>/start</b> — Главное меню  
🔹 <b>/help</b> — Показать справку
🔹 <b>/show_new_macs</b> — Показать список новых MAC-адресов  
🔹 <b>/bind_inv_to_mac</b> — Начать сопоставление MAC с инвентарными номерами
🔹 <b>/delete_user</b> — Удалить пользователя из системы. <b>Внимание</b>: текстовая команда может удалять <b>всех</b>!
🔹 <b>/user_list</b> — Показать список всех пользователей
🔹 <b>/reload_users</b> — Обновить данные пользователей из файла.

<b>💡 Формат допустимого инвентарного номера:</b>  
<code>12345</code> или <code>12345M</code>. Бот <b>автоматически</b> сформирует полное имя.
	""",
    "user": """
👋 <b>Добро пожаловать!</b>

С этим ботом вы можете:
🔎 Просматривать новые MAC-адреса  
🔗 Привязывать MAC к инвентарным номерам

Нажмите <b>/help</b> для получения справки по командам.

Выберите команду или воспользуйтесь меню ниже 👇
    """,
    "user_help": """
<b>📘 Справка по командам:</b>

🔹 <b>/start</b> — Главное меню  
🔹 <b>/help</b> — Показать справку
🔹 <b>/show_new_macs</b> — Показать список новых MAC-адресов  
🔹 <b>/bind_inv_to_mac</b> — Начать сопоставление MAC с инвентарными номерами

<b>💡 Формат допустимого инвентарного номера:</b>  
<code>12345</code> или <code>12345M</code>. Бот <b>автоматически</b> сформирует полное имя.
	""",
    "viewer": """
🔒 <b>Доступ ограничен.</b>

Вы не авторизованы для использования бота.

Обратитесь к администратору через кнопку ниже для получения доступа 👇

    """,
    "viewer_help": """
<b>🔐 Справка:</b>

Вы пока не авторизованы для работы с ботом.

<b>Что вы можете сделать:</b>  
— Просмотреть информацию о доступных командах  
— Запросить доступ к функциям бота через кнопку ниже

Для доступа к функциям бота необходимо разрешение.
""",
    "no_admins": "❗ Не удалось найти администраторов. Попробуйте позже.",
    "request_access_from_user": "👤 Пользователь <b>{full_name}</b> (ID: <code>{user_id}</code>) запросил доступ.",
    "request_access_sent": "📩 Заявка на доступ отправлена администраторам.",
    "no_access": "⛔ У вас недостаточно прав для выполнения этого действия.",
    "unknown_user": "❓ Без имени",
    "users_update": "🔄 Список пользователей обновлён из файла.",
    "empty_users": "📭 Список пользователей пуст.",
    "needs_id_for_delete": "❗ Укажите ID пользователя: <code>/delete_user 123456789</code>",
    "user_deleted": "✅ Пользователь <code>{user_id}</code> успешно удалён.",
    "user_not_found": "❌ Пользователь <code>{user_id}</code> не найден.",
    "note": "Добавлен администратором <code>{callback}</code> (<code>{admin_id}</code>)",
    "add_user": "✅ Пользователь <b>{full_name}</b> (<code>{user_id}</code>) был добавлен.",
    "approve_access": "🔓 Вам предоставлен доступ к боту. Приятного использования!",
    "user_already_exists": "❗ Пользователь <code>{user_id}</code> уже существует.",
    "admin_request_denied": "❌ Заявка отклонена.",
    "user_request_denied": "🚫 Ваша заявка на доступ была отклонена.",
    "only_admin": "⛔ Вы — единственный администратор. Удаление доступно после передачи прав либо через команду /delete_user.",
    "uncorrect_count": "⚠️ Число инвентарных ({inv_lines}) и MAC-адресов ({mac_list}) не совпадают.",
    "already_exists": [
        "⚠️ Обнаружены уже существующие имена ПК:\n",
        "\n\nВы уверены, что хотите сохранить эти данные?",
    ],
    "save_success": "✅ Сопоставления успешно сохранены.",
    "save_error": "❌ Не удалось сохранить данные. Обратитесь к администратору.",
    "bind_cancel": "❌ Привязка отменена.",
    "unknown_role": "❗ Неизвестная роль пользователя.",
    "no_notes": "Нет заметок.",
    "user_entry": "<b>{index}. {name}</b> (ID: <code>{user_id}</code>) — роль: <code>{role}</code>{note_part}\n",
    "no_new_macs": "🚫 Новых MAC-адресов не найдено.",
    "error_inv_format": [
        "⚠️ Найдены инвентарные номера с неправильным форматом:\n",
        "\n\nФормат должен быть <code>12345</code> или <code>12345M</code>. Пожалуйста, проверьте и повторите попытку.",
    ],
    "no_file": "🚫 Один из требуемых файлов не найден. Попробуйте позже.",
    "found_new_macs": [
        "Найдено {mac_list} MAC-адресов\n\n",
        "Отправьте список инвентарных номеров в ответ — один на строку.",
    ],
}

COMMANDS_DESC = {
    "start": "Запустить бота",
    "help": "Справка по боту",
    "bind_inv_to_mac": "Привязать Inv к MAC",
    "show_new_macs": "Показать новые MAC",
    "delete_user": "Удалить пользователя",
    "user_list": "Список пользователей",
    "reload_users": "Обновить пользователей",
}

BUTTONS = {
    "buttons": {
        "bind_inv_to_mac": "🔗 Привязать Inv к MAC",
        "show_new_macs": "🔎 Показать новые MAC",
        "delete_user": "🗑️ Удалить пользователя",
        "user_list": "📄 Список пользователей",
        "request_access": "🔑 Запросить доступ",
    },
    "approve": "✅ Подтвердить",
    "deny": "❌ Отклонить",
    "delete": "🗑️ Удалить",
    "confirm_save": "✅ Да, сохранить",
    "cancel_save": "❌ Нет, отмена",
}

# Template: role → list of button rows (row = list of buttons)
MENU_TEMPLATE = {
    "admin": [
        ["bind_inv_to_mac", "show_new_macs"],
        ["delete_user", "user_list"],
    ],
    "user": [
        ["bind_inv_to_mac", "show_new_macs"],
    ],
    "viewer": [
        ["request_access"],
    ],
}


def get_message(message: str) -> str:
    """
    Returns the welcome message based on the user's role.

    Args:
        message (str): The message key for the bot answer message.

    Returns:
        str: The message corresponding to the message key.
    """
    return MESSAGES.get(message, "❌ Сообщение не найдено.")  # type: ignore


def get_command_desc(command: str) -> str:
    """
    Returns the description of a command based on the command key.

    Args:
        command (str): The command key for the bot answer commands.

    Returns:
        str: The description of the command.
    """
    return COMMANDS_DESC.get(command, "❌ Команда не найдена.")  # type: ignore


def get_button(message: str) -> str:
    """
    Returns a text representation of buttons based on the button key.

    Args:
        message (str): The message key for the bot answer buttons.

    Returns:
        str: A text representation of the buttons.
    """
    return BUTTONS.get(message, "❌ Кнопка не найдена.")  # type: ignore


def get_menu_button(message: str) -> str:
    """
    Returns a text representation of menu buttons based on the button key.

    Args:
        message (str): The message key for the bot answer buttons.

    Returns:
        str: A text representation of the buttons.
    """
    return BUTTONS["buttons"].get(message, "❌ Кнопка не найдена.")  # type: ignore

from logging import Logger
from typing import Any

from utils.parser import (
    extract_new_macs,
    LOG_FILE,
    PROCESSED_MACS_FILE,
    FRESH_LIMIT_MINUTES,
)


def format_user_entry(
    user_id: int, user: dict[str, Any], index: int | None = None
) -> str:
    """
    Formats a user entry for display in a message.

    Args:
        user_id (int): The user's ID.
        user (dict[str, Any]): A dictionary containing user details.
        index (int | None): Optional index for numbering the user entry.
    Returns:
        str: Formatted user entry string.
    """
    name = user.get("full_name")
    role = user.get("role", "unknown")
    notes = user.get("notes", "заметок нет")
    # added_by = user.get("added_by", "неизвестно")

    prefix = f"{index}. " if index is not None else ""
    note_part = f"\n    📝 {notes}" if notes else ""
    # added_by_part = f" (добавлен: <code>{added_by}</code>)" if added_by else ""

    return (
        f"{prefix}<b>{name}</b> (ID: <code>{user_id}</code>) — "
        f"роль: <code>{role}</code>{note_part}\n"
    )


def safe_get_new_macs_text(logger: Logger) -> tuple[list[str] | None, str]:
    try:
        mac_list, text = format_new_macs_text(
            LOG_FILE, PROCESSED_MACS_FILE, FRESH_LIMIT_MINUTES
        )
        return mac_list, text
    except FileNotFoundError:
        logger.error(
            f"One of the required files not found: {LOG_FILE} or {PROCESSED_MACS_FILE}."
        )
        return None, "🚫 Один из требуемых файлов не найден. Попробуйте позже."


def format_new_macs_text(log_file, processed_file, fresh_limit_minutes):
    mac_list = extract_new_macs(log_file, processed_file, fresh_limit_minutes)

    if not mac_list:
        return None, "🚫 Новых MAC-адресов не найдено."

    text = "\n".join(f"{i+1}. {mac}" for i, mac in enumerate(mac_list))
    return mac_list, text

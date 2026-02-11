from typing import Any, Optional


def format_user_entry(
    user_id: int, user: dict[str, Any], index: Optional[int] = None
) -> str:
    """
    Formats a user entry for display in a message.

    This function creates a formatted string representing a user, including their full name,
    user ID, role, and any notes. An optional index can be provided for numbering the entry.

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

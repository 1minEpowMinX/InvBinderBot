from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from logging import Logger
from pathlib import Path
from pandas import DataFrame, concat, read_csv
from typing import Optional, Sequence

from fsm.binding import BindingInventory
from utils.formatting import format_new_macs_text
from utils.parser import (
    LOG_FILE,
    PROCESSED_MACS_FILE,
    FRESH_LIMIT_MINUTES,
)


def safe_get_new_macs_text(logger: Logger) -> tuple[Optional[list[str]], str]:
    """
    Safely retrieves new MAC addresses and formats them for display.

    Args:
        logger (Logger): The logger instance for logging events.
    Returns:
        tuple[Optional[list[str]], str]: A tuple containing a list of new MAC addresses and a formatted text message.
    """
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


async def handle_mac_action(
    message: Message,
    logger: Logger,
    action: str,
    state: FSMContext = None,  # type: ignore
) -> None:
    user_id = message.from_user.id  # type: ignore
    mac_list, text = safe_get_new_macs_text(logger)

    logger.info(
        f"User {message.from_user.full_name} ({user_id}) triggered MAC action: {action}."  # type: ignore
    )

    if mac_list is None:
        await message.answer(text)
        return

    if action == "show":
        await message.answer(f"Найдено {len(mac_list)} MAC-адресов:\n\n{text}")
        return

    if action == "bind" and state:
        await state.set_state(BindingInventory.waiting_for_inventory_numbers)
        await state.update_data(mac_list=mac_list, user_id=user_id)
        await message.answer(
            f"Найдено {len(mac_list)} MAC-адресов:\n\n{text}\n\n"
            "Отправьте список инвентарных номеров в ответ — один на строку."
        )


def save_macs_mapping(
    rows: Sequence[dict[str, str]],
    file_path: Path,
    logger: Logger,
) -> bool:
    """
    Saves the MAC-to-inventory mapping to the specified CSV file.

    Args:
        rows (Sequence[dict[str, str]]): List of {"MACAddress": ..., "ComputerName": ...} entries.
        file_path (Path): Path to the target CSV file.
        logger (Logger): Logger for logging events.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        try:
            df_existing = read_csv(file_path)
        except FileNotFoundError:
            df_existing = DataFrame()

        df_result = concat([df_existing, DataFrame(rows)], ignore_index=True)
        df_result.to_csv(file_path, index=False)
        logger.info(f"Saved {len(rows)} MAC-to-inventory rows to {file_path}")
        return True
    except Exception as e:
        logger.exception(f"Failed to save MAC mappings: {e}")
        return False

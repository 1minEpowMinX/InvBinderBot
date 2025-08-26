from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from logging import Logger
from os import getenv
from pathlib import Path
from pandas import DataFrame, concat, read_csv
from typing import Optional, Sequence

from fsm.binding import BindingInventory
from lexicon.lexicon import get_message
from utils.parser import extract_new_macs


LOG_FILE = Path(getenv("LOG_FILE", default="dhcp.log"))
PROCESSED_MACS_FILE = Path(getenv("PROCESSED_MACS", default="processed_macs.csv"))
FRESH_LIMIT_MINUTES = float(getenv("FRESH_LIMIT_MINUTES", default=5))
NAME_TEMPLATE = getenv("NAME_TEMPLATE", default="{}")


def safe_get_new_macs(logger: Logger) -> tuple[Optional[list[str]], int]:
    """
    Safely retrieves new MAC addresses and count them for display.

    Args:
        logger (Logger): The logger instance for logging events.
    Returns:
        tuple[Optional[list[str]], int]: A tuple containing a list of new MAC addresses and a count.
    """
    try:
        mac_list = extract_new_macs(
            LOG_FILE, PROCESSED_MACS_FILE, FRESH_LIMIT_MINUTES  # type: ignore
        )
        return mac_list, len(mac_list)
    except FileNotFoundError:
        logger.error(
            f"One of the required files not found: {LOG_FILE} or {PROCESSED_MACS_FILE}."
        )
        return None, 0


async def handle_mac_action(
    message: Message,
    logger: Logger,
    action: str,
    state: FSMContext = None,  # type: ignore
) -> None:
    user_id = message.from_user.id  # type: ignore
    mac_list, cnt = safe_get_new_macs(logger)

    logger.info(
        f"User {message.from_user.full_name} ({user_id}) triggered MAC action: {action}."  # type: ignore
    )

    if mac_list is None:
        await message.answer(get_message("no_new_macs"))
        return

    if action == "show":
        await message.answer(get_message("found_new_macs")[0].format(mac_list=cnt))
        return

    if action == "bind" and state:
        await state.set_state(BindingInventory.waiting_for_inventory_numbers)
        await state.update_data(mac_list=mac_list, user_id=user_id)
        await message.answer(
            get_message("found_new_macs")[0].format(mac_list=cnt)
            + get_message("found_new_macs")[1],
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

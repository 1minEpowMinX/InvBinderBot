from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from logging import Logger
from pathlib import Path
from pandas import DataFrame, concat, read_csv
from typing import Optional, Sequence

from config.config import MacBindingConfig
from fsm.binding import BindingInventory
from lexicon.lexicon import get_message
from utils.parser import extract_new_macs


def get_safe_new_macs(
    logger: Logger,
    log_file: Path,
    bound_computers_csv: Path,
    fresh_limit: float,
) -> tuple[Optional[list[str]], int]:
    """
    Safely retrieves new MAC addresses and count them for display.

    This function attempts to extract new MAC addresses from the log file,
    handling potential file not found errors gracefully.

    Args:
        logger (Logger): The logger instance for logging events.
        log_file (Path): Path to the log file containing MAC addresses.
        bound_computers_csv (Path): Path to the CSV file containing MAC addresses already bound to computers.
        fresh_limit (float): The freshness limit in minutes.

    Returns:
        tuple[Optional[list[str]], int]: A tuple containing a list of new MAC addresses and a count.
    """
    try:
        mac_list = extract_new_macs(
            log_file, bound_computers_csv, fresh_limit  # type: ignore
        )
        return mac_list, len(mac_list)
    except FileNotFoundError:
        logger.error(
            f"One of the required files not found: {log_file} or {bound_computers_csv}."
        )
        return None, 0


async def handle_mac_action(
    message: Message,
    logger: Logger,
    action: str,
    mac_binding: MacBindingConfig,
    state: FSMContext = None,  # type: ignore
) -> None:
    """
    Handles actions related to MAC addresses.

    This function retrieves new MAC addresses and checks the action type. If the action is "show",
    it sends a message with the count of new MACs. If the action is "bind", it sets the FSM state to wait for inventory number

    Args:
        message (Message): The incoming message that triggered the action.
        logger (Logger): The logger instance for logging events.
        action (str): The action to be performed (e.g., "show" or "bind").
        mac_binding (MacBindingConfig): Configuration for MAC binding, file paths, and related parameters.
        state (FSMContext): The finite state machine context for managing user sessions.
    """
    user_id = message.from_user.id  # type: ignore
    mac_list, cnt = get_safe_new_macs(
        logger,
        mac_binding.dhcp_log,
        mac_binding.bound_computers_csv,
        mac_binding.fresh_limit,
    )

    if mac_list is None:
        await message.answer(get_message("no_file"))
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
    bound_computers_csv: Path,
    logger: Logger,
) -> bool:
    """
    Saves the MAC-to-inventory mapping to the specified CSV file.

    This function appends the provided rows to an existing CSV file or creates a new file if it doesn't exist.

    Args:
        rows (Sequence[dict[str, str]]): List of {"MACAddress": ..., "ComputerName": ...} entries.
        bound_computers_csv (Path): Path to the CSV file with already bound MAC addresses
        logger (Logger): Logger for logging events.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        try:
            df_existing = read_csv(bound_computers_csv)
        except FileNotFoundError:
            df_existing = DataFrame()

        df_result = concat([df_existing, DataFrame(rows)], ignore_index=True)
        df_result.to_csv(bound_computers_csv, index=False)

        logger.info(f"Saved {len(rows)} MAC-to-inventory rows to {bound_computers_csv}")
        return True
    except Exception as e:
        logger.exception(f"Failed to save MAC mappings: {e}")
        return False

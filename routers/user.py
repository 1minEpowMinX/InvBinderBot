import pandas as pd
from aiogram import Router, F
from aiogram.types import Message
from logging import Logger

from utils.formatting import safe_get_new_macs_text

router = Router()

# Session storage for active MAC binding sessions
active_mac_sessions: dict[int, list[str]] = {}


@router.message(F.text == "🔎 Показать новые MAC")
async def show_new_macs(message: Message, logger: Logger):
    """Handles the command to show new MAC addresses.
        This function retrieves new MAC addresses from the log file and sends them to the user.
    Args:
        message (Message): The incoming message that triggered the command.
        logger (Logger): The logger instance for logging events.
    """
    logger.info(
        f"User {message.from_user.full_name} ({message.from_user.id}) requested new MAC addresses."  # type: ignore
    )
    _, text = safe_get_new_macs_text(logger)
    await message.answer(text)


@router.message(F.text == "🔗 Привязать Inv к MAC")
async def start_mac_binding(message: Message, logger: Logger):
    """
    Starts the process of binding inventory numbers to MAC addresses.
    This function initiates a session where the user can provide inventory numbers
    corresponding to newly detected MAC addresses.

    Args:
        message (Message): The incoming message that triggered the command.
        logger (Logger): The logger instance for logging events.
    """
    user_id = message.from_user.id  # type: ignore

    mac_list, text = safe_get_new_macs_text(logger)

    logger.info(
        f"User {message.from_user.full_name} ({user_id}) started MAC binding session."  # type: ignore
    )

    if mac_list is None:
        await message.answer(text)
        return

    active_mac_sessions[user_id] = mac_list
    await message.answer(
        f"Найдено {len(mac_list)} MAC-адресов:\n\n{text}\n\n"
        "Отправьте список инвентарных номеров в ответ - один на строку."
    )


@router.message()
async def handle_inventory_reply(message: Message, logger: Logger):
    """
    Handles the user's reply with inventory numbers.
    Expects the user to have an active session with MAC addresses.

    Args:
        message (Message): The incoming message containing inventory numbers.
        logger (Logger): The logger instance for logging events.

    """
    user_id = message.from_user.id  # type: ignore
    if user_id not in active_mac_sessions:
        logger.warning(
            f"User {message.from_user.full_name} ({user_id}) attempted to bind inventory numbers without an active session."  # type: ignore
        )
        return

    mac_list = active_mac_sessions.pop(user_id)
    inv_lines = message.text.strip().splitlines()  # type: ignore

    if len(inv_lines) != len(mac_list):
        logger.warning(
            f"User {message.from_user.full_name} ({user_id}) provided mismatched inventory numbers and MAC addresses."  # type: ignore
        )
        await message.answer(
            f"⚠️ Число инвентарных ({len(inv_lines)}) и MAC-адресов ({len(mac_list)}) не совпадают."
        )
        return

    rows = [
        {"MACAddress": mac, "Inv": inv.strip()} for mac, inv in zip(mac_list, inv_lines)
    ]

    try:
        df_old = pd.read_csv(PROCESSED_MACS_FILE)
        df_new = pd.concat([df_old, pd.DataFrame(rows)], ignore_index=True)
    except FileNotFoundError:
        logger.error(
            f"Processed MACs file {PROCESSED_MACS_FILE} not found. Creating a new one."
        )
        df_new = pd.DataFrame(rows)

    df_new.to_csv(PROCESSED_MACS_FILE, index=False)
    await message.answer("✅ Сопоставления сохранены.")

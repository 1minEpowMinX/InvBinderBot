import pandas as pd
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from logging import Logger

from fsm.binding import BindingInventory
from keyboards.confirmation import get_one_time_keyboard
from keyboards.reply import get_menu_by_role
from utils.mac_utils import handle_mac_action
from utils.parser import PROCESSED_MACS_FILE
from utils.validation import validate_inv_format


router = Router()


@router.message(F.text == "🔎 Показать новые MAC")
async def show_new_macs(message: Message, logger: Logger) -> None:
    """
    Handles the command to show new MAC addresses.

    This function retrieves new MAC addresses from the log file and sends them to the user.

    Args:
        message (Message): The incoming message that triggered the command.
        logger (Logger): The logger instance for logging events.
    """
    await handle_mac_action(message, logger, action="show")


@router.message(F.text == "🔗 Привязать Inv к MAC")
async def start_mac_binding(
    message: Message, state: FSMContext, logger: Logger
) -> None:
    """
    Initiates the binding process of inventory numbers to MAC addresses.

    This function sets the state to waiting for inventory numbers and updates the context with the MAC list.

    Args:
        message (Message): The incoming message that triggered the binding command.
        state (FSMContext): The finite state machine context for managing user sessions.
        logger (Logger): The logger instance for logging events.
    """
    await handle_mac_action(message, logger, action="bind", state=state)


@router.message(BindingInventory.waiting_for_inventory_numbers)
async def handle_inventory_reply(message: Message, state: FSMContext, logger: Logger):
    """
    Handles the user's reply containing inventory numbers.

    This function processes the inventory numbers provided by the user,
    checks for duplicates against existing records, and either saves the data
    or prompts the user for confirmation if duplicates are found.

    Args:
        message (Message): The incoming message containing inventory numbers.
        state (FSMContext): The finite state machine context for managing user sessions.
        logger (Logger): The logger instance for logging events.

    """
    data = await state.get_data()
    user_id = message.from_user.id  # type: ignore
    if user_id != data["user_id"]:
        logger.warning(
            f"User {message.from_user.full_name} ({user_id}) attempted to bind inventory numbers without an active session."  # type: ignore
        )
        return

    mac_list: list[str] = data["mac_list"]
    inv_lines = message.text.strip().splitlines()  # type: ignore
    if not await validate_inv_format(inv_lines, message, logger):
        return

    if len(inv_lines) != len(mac_list):
        logger.warning(
            f"User {message.from_user.full_name} ({user_id}) provided mismatched inventory numbers and MAC addresses."  # type: ignore
        )
        await message.answer(
            f"⚠️ Число инвентарных ({len(inv_lines)}) и MAC-адресов ({len(mac_list)}) не совпадают."
        )
        return

    df_existing = pd.DataFrame()
    try:
        df_existing = pd.read_csv(PROCESSED_MACS_FILE)
    except FileNotFoundError:
        logger.error(f"Processed MACs file {PROCESSED_MACS_FILE} not found.")

    duplicates: list[str] = []
    rows: list[dict[str, str]] = []
    for mac, inv in zip(mac_list, inv_lines):
        inv = inv.strip()
        rows.append({"MACAddress": mac, "ComputerName": inv})
        if not df_existing.empty and inv in df_existing["ComputerName"].values:
            duplicates.append(inv)

    if duplicates:
        logger.warning(
            f"User {message.from_user.full_name} ({user_id}) attempted to bind duplicate inventory numbers: {', '.join(duplicates)}."  # type: ignore
        )
        await state.update_data(pending_rows=rows)
        await state.set_state(BindingInventory.waiting_for_confirmation)

        text = [
            "✅ Да, сохранить",
            "❌ Нет, отмена",
        ]
        await message.answer(
            "⚠️ Обнаружены уже существующие имена ПК:\n"
            + "\n".join(f"- {inv}" for inv in duplicates)
            + "\n\nВы уверены, что хотите сохранить эти данные?",
            reply_markup=get_one_time_keyboard(text),
        )
    else:
        df_result = pd.concat([df_existing, pd.DataFrame(rows)], ignore_index=True)
        df_result.to_csv(PROCESSED_MACS_FILE, index=False)
        await state.clear()
        await message.answer("✅ Сопоставления сохранены.")


@router.message(BindingInventory.waiting_for_confirmation, F.text == "✅ Да, сохранить")
async def confirm_save(message: Message, role: str, state: FSMContext, logger: Logger):
    """
    Confirms the saving of inventory numbers and MAC addresses.

    This function retrieves the pending rows from the state, saves them to the processed MACs file,
    and clears the state.
    Args:
        message (Message): The incoming message confirming the save action.
        state (FSMContext): The finite state machine context for managing user sessions.
        logger (Logger): The logger instance for logging events.
    """
    data = await state.get_data()
    pending_rows = data.get("pending_rows", [])
    try:
        df_existing = pd.read_csv(PROCESSED_MACS_FILE)
    except FileNotFoundError:
        logger.error(f"Processed MACs file {PROCESSED_MACS_FILE} not found.")
        df_existing = pd.DataFrame()

    df_result = pd.concat([df_existing, pd.DataFrame(pending_rows)], ignore_index=True)
    df_result.to_csv(PROCESSED_MACS_FILE, index=False)

    logger.info(
        f"User {message.from_user.full_name} ({message.from_user.id}) confirmed saving duplicated inventory numbers."  # type: ignore
    )

    await state.clear()
    await message.answer("✅ Сопоставления сохранены.", reply_markup=get_menu_by_role(role))  # type: ignore


@router.message(F.text == "❌ Нет, отмена")
async def cancel_binding(
    message: Message, role: str, state: FSMContext, logger: Logger
):
    """
    Cancels the binding process of inventory numbers to MAC addresses.

    This function clears the current state and informs the user that the operation has been canceled.

    Args:
            message (Message): The incoming message indicating cancellation.
            state (FSMContext): The finite state machine context for managing user sessions.
            logger (Logger): The logger instance for logging events.
    """
    await state.clear()
    logger.info(
        f"User {message.from_user.full_name} ({message.from_user.id}) canceled the binding duplicated inventory numbers process"  # type: ignore
    )
    await message.answer("❌ Привязка отменена.", reply_markup=get_menu_by_role(role))  # type: ignore

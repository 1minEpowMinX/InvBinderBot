from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, or_f
from aiogram.types import Message
from logging import Logger
from pandas import DataFrame, read_csv

from config.config import FilesConfig
from fsm.binding import BindingInventory
from keyboards.confirmation import get_one_time_keyboard
from keyboards.reply import get_menu_by_role
from lexicon.lexicon import get_message, get_button, get_menu_button
from utils.mac_utils import handle_mac_action, save_macs_mapping
from utils.validation import validate_inv_format


router = Router()


@router.message(or_f(Command("bind_inv_to_mac"), F.text == get_menu_button("bind_inv_to_mac")))  # type: ignore
async def start_mac_binding(
    message: Message, state: FSMContext, logger: Logger, config_files: FilesConfig
) -> None:
    """
    Initiates the binding process of inventory numbers to MAC addresses.

    This function sets the state to waiting for inventory numbers and updates the context with the MAC list.

    Args:
        message (Message): The incoming message that triggered the binding command.
        state (FSMContext): The finite state machine context for managing user sessions.
        logger (Logger): The logger instance for logging events.
        files_config (FilesConfig): An instance of FilesConfig containing file paths.
    """
    await handle_mac_action(
        message, logger, action="bind", state=state, config_files=config_files
    )


@router.message(or_f(Command("show_new_macs"), F.text == get_menu_button("show_new_macs")))  # type: ignore
async def show_new_macs(
    message: Message, logger: Logger, config_files: FilesConfig
) -> None:
    """
    Handles the command to show new MAC addresses.

    This function retrieves new MAC addresses from the log file and sends them to the user.

    Args:
        message (Message): The incoming message that triggered the command.
        logger (Logger): The logger instance for logging events.
        config_files (FilesConfig): An instance of FilesConfig containing file paths.
    """
    await handle_mac_action(message, logger, action="show", config_files=config_files)


@router.message(BindingInventory.waiting_for_inventory_numbers)
async def handle_inventory_reply(
    message: Message,
    role: str,
    state: FSMContext,
    logger: Logger,
    config_files: FilesConfig,
):
    """
    Handles the user's reply containing inventory numbers.

    This function processes the inventory numbers provided by the user,
    checks for duplicates against existing records, and either saves the data
    or prompts the user for confirmation if duplicates are found.

    Args:
        message (Message): The incoming message containing inventory numbers.
        role (str): The role of the user, used for determining access permissions.
        state (FSMContext): The finite state machine context for managing user sessions.
        logger (Logger): The logger instance for logging events.
        config_files (FilesConfig): An instance of FilesConfig containing file paths.

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
            get_message("uncorrect_count").format(
                inv_lines=len(inv_lines), mac_list=len(mac_list)
            )
        )
        return

    df_existing = DataFrame()
    try:
        df_existing = read_csv(config_files.processed_macs)
    except FileNotFoundError:
        logger.error(f"Processed MACs file {config_files.processed_macs} not found.")

    duplicates: list[str] = []
    rows: list[dict[str, str]] = []
    for mac, inv in zip(mac_list, inv_lines):
        inv = config_files.name_template + inv.strip()
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
            get_button("confirm_save"),
            get_button("cancel_save"),
        ]
        await message.answer(
            get_message("already_exists")[0]
            + "\n".join(f"- {inv}" for inv in duplicates)
            + get_message("already_exists")[1],
            reply_markup=get_one_time_keyboard(text),
        )
    else:
        if save_macs_mapping(rows, config_files.processed_macs, logger):
            await state.clear()
            await message.answer(get_message("save_success"), reply_markup=get_menu_by_role(role))  # type: ignore
        else:
            await message.answer(get_message("save_error"), reply_markup=get_menu_by_role(role))  # type: ignore


@router.message(BindingInventory.waiting_for_confirmation, F.text == get_button("confirm_save"))  # type: ignore
async def confirm_save(
    message: Message,
    role: str,
    state: FSMContext,
    logger: Logger,
    config_files: FilesConfig,
):
    """
    Confirms the saving of inventory numbers and MAC addresses.

    This function retrieves the pending rows from the state, saves them to the processed MACs file,
    and clears the state.
    Args:
        message (Message): The incoming message confirming the save action.
        state (FSMContext): The finite state machine context for managing user sessions.
        logger (Logger): The logger instance for logging events.
        config_files (FilesConfig): An instance of FilesConfig containing file paths.
    """
    data = await state.get_data()
    pending_rows = data.get("pending_rows", [])

    logger.info(
        f"User {message.from_user.full_name} ({message.from_user.id}) confirmed saving duplicated inventory numbers."  # type: ignore
    )

    if save_macs_mapping(pending_rows, config_files.processed_macs, logger):
        await state.clear()
        await message.answer(get_message("save_success"), reply_markup=get_menu_by_role(role))  # type: ignore
    else:
        await message.answer(get_message("save_error"))


@router.message(F.text == get_button("cancel_save"))  # type: ignore
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
    await message.answer(get_message("bind_cancel"), reply_markup=get_menu_by_role(role))  # type: ignore

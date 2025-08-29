from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup

from lexicon.lexicon import get_message

router = Router()


@router.message(Command("start"))
async def start_handler(
    message: Message, role: str, keyboard: ReplyKeyboardMarkup
) -> None:
    """
    Sends a welcome message and displays the menu based on the user's role.

    This function retrieves the user's role and sends a personalized welcome message
    along with a keyboard menu tailored to their permissions.

    Args:
        message (Message): The incoming message that triggered the command.
        role (str): The role of the user.
        keyboard (ReplyKeyboardMarkup): The keyboard markup for the menu.
    """

    await message.answer(get_message(role), reply_markup=keyboard)


@router.message(Command("help"))
async def help_handler(
    message: Message, role: str, keyboard: ReplyKeyboardMarkup
) -> None:
    """
    Provides help information based on the user's role.

    This function retrieves the user's role and sends a help message
    tailored to their permissions, along with the appropriate keyboard menu.

    Args:
        message (Message): The incoming message that triggered the command.
        role (str): The role of the user.
        keyboard (ReplyKeyboardMarkup): The keyboard markup for the menu.
    """

    await message.answer(get_message(f"{role}_help"), reply_markup=keyboard)

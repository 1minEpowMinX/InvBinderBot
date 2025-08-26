from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup

from lexicon.lexicon import get_message

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, role: str, keyboard: ReplyKeyboardMarkup):
    await message.answer(get_message(role), reply_markup=keyboard)


@router.message(Command("help"))
async def help_handler(message: Message, role: str, keyboard: ReplyKeyboardMarkup):
    await message.answer(get_message(f"{role}_help"), reply_markup=keyboard)

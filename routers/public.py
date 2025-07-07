from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, role: str, keyboard: ReplyKeyboardMarkup):
    await message.answer(f"Добро пожаловать! Ваша роль: {role}", reply_markup=keyboard)


@router.message(Command("help"))
async def help_handler(message: Message, role: str, keyboard: ReplyKeyboardMarkup):
    help_text = "Заглушка для команды /help\n\n"
    await message.answer(help_text, reply_markup=keyboard)

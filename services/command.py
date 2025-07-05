from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat
from utils.auth_manager import AuthManager


async def assign_role_commands(bot: Bot, auth: AuthManager):
    """
    Sets role-based commands for each user based on their role.

    Args:
        bot (Bot): The bot instance to set commands for.
        auth (AuthManager): The authorization manager to control user roles.
    """
    for user_id in auth.get_list_users().keys():
        role = auth.get_role(user_id)
        commands = [BotCommand(command="start", description="Запустить бота")]

        if role == "admin":
            commands += [
                BotCommand(command="users", description="Список пользователей"),
                BotCommand(command="add", description="Добавить пользователя"),
            ]
        elif role == "user":
            commands += [
                BotCommand(command="help", description="Справка по боту"),
            ]

        await bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id=user_id))

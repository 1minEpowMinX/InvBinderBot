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

        if role != "viewer":
            commands += [
                BotCommand(command="help", description="Справка по боту"),
                BotCommand(
                    command="bind_inv_to_mac", description="Привязать Inv к MAC"
                ),
                BotCommand(command="show_new_macs", description="Показать новые MAC"),
            ]

        if role == "admin":
            commands += [
                BotCommand(command="delete_user", description="Удалить пользователя"),
                BotCommand(command="user_list", description="Список пользователей"),
                BotCommand(
                    command="reload_users", description="Обновить пользователей"
                ),
            ]

        await bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id=user_id))

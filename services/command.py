from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat

from lexicon.lexicon import get_command_desc
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
        commands = [BotCommand(command="start", description=get_command_desc("start"))]

        if role != "viewer":
            commands += [
                BotCommand(command="help", description=get_command_desc("help")),
                BotCommand(
                    command="bind_inv_to_mac",
                    description=get_command_desc("bind_inv_to_mac"),
                ),
                BotCommand(
                    command="show_new_macs",
                    description=get_command_desc("show_new_macs"),
                ),
            ]

        if role == "admin":
            commands += [
                BotCommand(
                    command="delete_user", description=get_command_desc("delete_user")
                ),
                BotCommand(
                    command="user_list", description=get_command_desc("user_list")
                ),
                BotCommand(
                    command="reload_users", description=get_command_desc("reload_users")
                ),
            ]

        await bot.set_my_commands(commands, scope=BotCommandScopeChat(chat_id=user_id))

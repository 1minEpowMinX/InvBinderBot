import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config.config import Config, load_config
from middlewares.authorization_middleware import AuthMiddleware
from middlewares.logging_middleware import LoggingMiddleware
from routers import (
    access,
    admin,
    callbacks,
    public,
    user,
)
from services.command import assign_role_commands
from utils.auth_manager import AuthManager
from utils.logger import setup_logger

# Initialize logger and auth manager
auth_manager = AuthManager()
logger = setup_logger()


async def main() -> None:
    """
    Main function to configure and start the bot.
    """

    logger.info("Starting bot")
    config: Config = load_config()

    logger.info("Loading Redis storage")
    storage = config.redis.create_storage()
    redis = storage.redis

    if await redis.ping():
        logger.info("Redis storage is connected successfully")
    else:
        logger.error("Failed to connect to Redis storage")
        exit(1)

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    logger.info("Initializing Dispatcher")
    dp = Dispatcher(storage=storage, config_files=config.files)

    # Register middlewares
    logger.info("Registering middlewares")
    dp.message.middleware(LoggingMiddleware(logger))
    dp.message.middleware(AuthMiddleware(auth_manager))

    dp.callback_query.middleware(LoggingMiddleware(logger))
    dp.callback_query.middleware(AuthMiddleware(auth_manager))

    # Register routers in the dispatcher
    logger.info("Registering routers")
    dp.include_router(public.router)
    dp.include_router(access.router)
    dp.include_router(callbacks.router)
    dp.include_router(user.router)
    dp.include_router(admin.router)

    # Register commands for each user based on their role
    logger.info("Assigning role-based commands")
    await assign_role_commands(bot, auth_manager)

    # Drops webhook if it exists and switches to getUpdates
    # If there were updates while the bot was off, they will be skipped
    logger.info("Starting polling")
    await bot.delete_webhook(drop_pending_updates=True)
    # start polling with only allowed updates
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())

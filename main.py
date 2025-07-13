import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

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
    """Main function to configure and start the bot."""

    logger.info("Starting bot")
    config: Config = load_config()

    logger.info("Loading Redis storage")
    redis = Redis(host="localhost", port=6379)
    storage = RedisStorage(redis)

    if await redis.ping():
        logger.info("Redis storage is connected successfully")
    else:
        logger.error("Failed to connect to Redis storage")
        exit(1)

    bot = Bot(
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        token=config.tg_bot.token,
    )
    dp = Dispatcher(storage=storage)

    # Register middlewares
    logger.info("Registering middlewares")

    dp.message.middleware(LoggingMiddleware(logger))
    dp.message.middleware(AuthMiddleware(auth_manager))

    dp.callback_query.middleware(LoggingMiddleware(logger))
    dp.callback_query.middleware(AuthMiddleware(auth_manager))

    # Register routers in the dispatcher
    dp.include_router(public.router)
    dp.include_router(access.router)
    dp.include_router(callbacks.router)
    dp.include_router(user.router)
    dp.include_router(admin.router)

    # Register commands for each user based on their role
    logger.info("Assigning role-based commands")
    await assign_role_commands(bot, auth_manager)

    # Drops webhook if it exists and switches to getUpdates
    # If there were updates while the bot was off, they will be processed
    await bot.delete_webhook(drop_pending_updates=False)
    # start polling with only allowed updates
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())

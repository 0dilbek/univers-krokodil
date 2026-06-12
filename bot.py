import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from tortoise import Tortoise

from config import TORTOISE_ORM, load_settings
from handlers import router
from middlewares.delete_commands import DeleteCommandMiddleware
from services.bot_commands import setup_bot_commands
from services.game_watchdog import chat_refresh_loop, restore_active_games_on_startup, watchdog_loop


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = load_settings()
    if not settings.bot_token:
        raise RuntimeError("BOT_TOKEN env o'zgaruvchisini kiriting.")
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL env o'zgaruvchisini kiriting.")

    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)
    await restore_active_games_on_startup()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.message.middleware(DeleteCommandMiddleware())
    dp.include_router(router)
    await setup_bot_commands(bot)
    asyncio.create_task(watchdog_loop())
    asyncio.create_task(chat_refresh_loop(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

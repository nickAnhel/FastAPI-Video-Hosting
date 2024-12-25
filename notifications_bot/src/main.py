import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault

from config import settings
from router import router


async def main() -> None:
    bot = Bot(token=settings.token)
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Start using bot and verify account"),
            BotCommand(command="verify", description="Verify your Telegram account"),
        ],
        BotCommandScopeDefault(),
    )

    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

import asyncio
import logging

from database.database import database

from handlers import private_router
from handlers.group import group_router

from bot_config import bot, dp, database

async def on_startup(bot):
    database.create_tables()

async def main():
    dp.include_router(private_router)
    dp.include_router(group_router)

    dp.startup.register(on_startup)
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

import asyncio
import logging

from database.database import database
from handlers.other_messages import other_message
from handlers.picture import picture_router
from handlers.start import start_router
from handlers.random import random_router
from handlers.my_info import myinfo_router
from handlers.review_dialog import review_router
from bot_config import bot, dp, database

async def on_startup(bot):
    database.create_tables()


async def main():
    dp.include_router(random_router)
    dp.include_router(start_router)
    dp.include_router(myinfo_router)
    dp.include_router(picture_router)
    dp.include_router(review_router)
    dp.include_router(other_message)

    dp.startup.register(on_startup)
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

from aiogram import Router, types
from aiogram.filters import Command

from bot_config import database

dish_router = Router()

@dish_router.message(Command("dishes"))
async def show_all_dishes(message: types.Message):
    dishes = database.fetch(
        """
        SELECT d.name AS dish_name, d.price, c.name AS category_name
        FROM dish d
        JOIN dish_categories c ON d.category_id = c.id
        """
    )

    if not dishes:
        await message.answer("В каталоге пока нет блюд.")
        return


    await message.answer("Блюда из нашего каталога:")
    for dish in dishes:
        await message.answer(
            f"Категория: {dish['category_name']}\n"
            f"Название: {dish['dish_name']}\n"
            f"Цена: {dish['price']} баксов"
        )

from aiogram import F,Router,types
from aiogram.filters import Command

from bot_config import database

dish_router = Router()

@dish_router.message(Command("dishes"))
async def show_all_dishes(message: types.Message):
    dishes = database.fetch(
        query="SELECT * FROM dish"
    )
    print(dishes)
    await message.answer("Food from our catalog")
    for dish in dishes:
        await message.answer(f"Name: {dish['name']} \n Price: {dish['price']}")
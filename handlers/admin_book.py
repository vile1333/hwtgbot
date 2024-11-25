from aiogram import types,F,Router
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from bot_config import database

admin_dish_router = Router()
admin_dish_router.message.filter(
    F.from_user.id == 7677226191
)

class Dish(StatesGroup):
    name = State()
    price = State()

@admin_dish_router.message(Command('newdish'), default_state)
async def new_dish(message: types.Message,state: FSMContext):
    await state.set_state(Dish.name)
    await message.answer('New Dish')

@admin_dish_router.message(Dish.name)
async def process_name(message: types.Message,state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Dish.price)
    await message.answer('Price')

@admin_dish_router.message(Dish.price)
async def process_price(message: types.Message,state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Added sucessfully")
    data = await state.get_data()
    database.execute(
        query="""
        INSERT INTO dish(name,price)
        VALUES(?,?)
        """,
        params=
        (
            data['name'],
            data['price']
        )
    )


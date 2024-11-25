from aiogram import Router, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot_config import database


admin_dish_router = Router()
admin_dish_router.message.filter(
    F.from_user.id == 7677226191
)
# Состояния для FSM
class Category(StatesGroup):
    name = State()

class Dish(StatesGroup):
    category = State()
    name = State()
    price = State()


@admin_dish_router.message(Command('newcategory'))
async def new_category(message: types.Message, state: FSMContext):
    await state.set_state(Category.name)
    await message.answer('Введите название новой категории:')

@admin_dish_router.message(Category.name)
async def process_category_name(message: types.Message, state: FSMContext):
    category_name = message.text.strip()
    try:
        database.execute(
            """
            INSERT INTO dish_categories (name)
            VALUES (?)
            """,
            (category_name,)
        )
        await message.answer(f"Категория '{category_name}' успешно добавлена!")
    except Exception as e:
        await message.answer(f"Ошибка при добавлении категории: {e}")
    finally:
        await state.clear()

@admin_dish_router.message(Command('newdish'))
async def new_dish(message: types.Message, state: FSMContext):

    categories = database.fetch("SELECT name FROM dish_categories")

    if not categories:
        await message.answer("Нет доступных категорий. Добавьте категорию через /newcategory.")
        return


    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=category['name'])] for category in categories],
        resize_keyboard=True
    )

    await message.answer("Выберите категорию для нового блюда:", reply_markup=keyboard)
    await state.set_state(Dish.category)

@admin_dish_router.message(Dish.category)
async def process_dish_category(message: types.Message, state: FSMContext):
    category_name = message.text.strip()
    category = database.fetch(
        "SELECT id FROM dish_categories WHERE name = ?",
        (category_name,)
    )

    if not category:
        await message.answer("Неверная категория. Попробуйте снова.")
        return

    await state.update_data(category_id=category[0]['id'])
    await state.set_state(Dish.name)
    await message.answer("Введите название нового блюда:", reply_markup=types.ReplyKeyboardRemove())

@admin_dish_router.message(Dish.name)
async def process_dish_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Dish.price)
    await message.answer("Введите цену блюда:")

@admin_dish_router.message(Dish.price)
async def process_dish_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text.strip())
        await state.update_data(price=price)
        data = await state.get_data()

        database.execute(
            """
            INSERT INTO dish (name, price, category_id)
            VALUES (?, ?, ?)
            """,
            (data['name'], data['price'], data['category_id'])
        )

        await message.answer(f"Блюдо '{data['name']}' успешно добавлено!")
    except ValueError:
        await message.answer("Цена должна быть числом. Попробуйте снова.")
    except Exception as e:
        await message.answer(f"Ошибка при добавлении блюда: {e}")
    finally:
        await state.clear()

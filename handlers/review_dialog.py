from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from bot_config import database

review_router = Router()

# FSM - Состояния
class RestaurantReview(StatesGroup):
    name = State()
    phone_number = State()
    ig_username = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comment = State()

reviewed_users = set()  # Для проверки уникальности отзыва

# Начало опроса
@review_router.callback_query(F.data == 'review')
async def start_opros(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.from_user.id in reviewed_users:
        await callback_query.answer('Нельзя оставлять больше одного отзыва!')
        await state.clear()
    else:
        await state.set_state(RestaurantReview.name)
        await callback_query.message.answer('Как Вас зовут?')
        await callback_query.answer()

# Обработка имени
@review_router.message(RestaurantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RestaurantReview.phone_number)
    await message.answer('Напишите Ваш номер телефона')

# Обработка телефона
@review_router.message(RestaurantReview.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(RestaurantReview.ig_username)
    await message.answer('Ваш IG')

# Обработка Instagram
@review_router.message(RestaurantReview.ig_username)
async def process_ig_username(message: types.Message, state: FSMContext):
    await state.update_data(ig_username=message.text)
    await state.set_state(RestaurantReview.visit_date)
    await message.answer('Когда вы последний раз посещали нашу пиццерию? Введите в формате ГГГГ-MM-ДД')

# Обработка даты посещения
@review_router.message(RestaurantReview.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    date_parts = message.text.split('-')
    if len(date_parts) == 3 and all(part.isdigit() for part in date_parts):
        year, month, day = map(int, date_parts)
        if 1 <= month <= 12 and 1 <= day <= 31:
            await state.update_data(visit_date=message.text)
            await state.set_state(RestaurantReview.food_rating)
            kb_for_rating = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=str(i), callback_data=f'food_rating_{i}') for i in range(1, 6)]
                ]
            )
            await message.answer('Какую оценку вы поставите нашей пицце?', reply_markup=kb_for_rating)
            return
    await message.answer("Некорректная дата. Введите в формате ГГГГ-MM-ДД, например 2024-11-25.")

# Обработка оценки пиццы
@review_router.callback_query(RestaurantReview.food_rating, F.data.startswith('food_rating_'))
async def process_food_rating(callback_query: types.CallbackQuery, state: FSMContext):
    rating = callback_query.data.split('_')[2]
    await state.update_data(food_rating=rating)
    await state.set_state(RestaurantReview.cleanliness_rating)
    await callback_query.answer()

    kb_for_clean_rate = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=str(i), callback_data=f'cleanliness_rating_{i}') for i in range(1, 6)]
        ]
    )
    await callback_query.message.answer('Какую оценку вы поставите чистоте в нашей пиццерии?', reply_markup=kb_for_clean_rate)

# Обработка оценки чистоты
@review_router.callback_query(RestaurantReview.cleanliness_rating, F.data.startswith('cleanliness_rating_'))
async def process_cleanliness_rating(callback_query: types.CallbackQuery, state: FSMContext):
    rating = callback_query.data.split('_')[2]
    await state.update_data(cleanliness_rating=rating)
    await state.set_state(RestaurantReview.extra_comment)
    await callback_query.answer()
    await callback_query.message.answer('Есть ли какие-нибудь дополнения?')

# Обработка дополнительных комментариев
@review_router.message(RestaurantReview.extra_comment)
async def process_extra_comment(message: types.Message, state: FSMContext):
    await state.update_data(extra_comment=message.text)
    reviewed_users.add(message.from_user.id)
    data = await state.get_data()

    # Сохранение данных в базу
    database.execute(
        query="""
        INSERT INTO reviews(
            name1, phone_number, ig_username, visit_date, food_rating, cleanliness_rating, extra_comment
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        params=(
            data["name"],
            data["phone_number"],
            data["ig_username"],
            data["visit_date"],
            int(data["food_rating"]),
            int(data["cleanliness_rating"]),
            data["extra_comment"]
        )
    )

    await state.clear()
    await message.answer("Спасибо за ваш отзыв!", reply_markup=ReplyKeyboardRemove())

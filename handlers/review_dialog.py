from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from handlers.start import start_router

review_router = Router()


# фсм - finite state mashina
class RestorauntReview(StatesGroup):
    name = State()
    phone_number = State()
    ig_username = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comment = State()

reviewed_users = set() # Допка

@start_router.callback_query(F.data == 'review')
async def start_opros(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.from_user.id in reviewed_users:
        await callback_query.answer('Нельзя оставлять больше одного отзыва!')
        await state.clear()
    else:
        await state.set_state(RestorauntReview.name)
        await callback_query.message.answer('Как Вас зовут?')
        await callback_query.answer()

@review_router.message(RestorauntReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RestorauntReview.phone_number)
    await message.answer('Напишите Ваш номер телефона')


@review_router.message(RestorauntReview.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(RestorauntReview.ig_username)
    await message.answer('Ваш IG')


@review_router.message(RestorauntReview.ig_username)
async def process_ig_username(message: types.Message, state: FSMContext):
    await state.update_data(ig_username=message.text)
    await state.set_state(RestorauntReview.visit_date)
    await message.answer('Когда вы последний раз посещали нашу пиццерию?')


@review_router.message(RestorauntReview.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    await state.update_data(visit_date=message.text)
    await state.set_state(RestorauntReview.food_rating)
    kbforrating = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=str(i), callback_data=f'food_rating_{i}') for i in range(1, 6)]
        ]
    )
    await message.answer('Какую оценку вы поставите нашей пицце?', reply_markup=kbforrating)


@review_router.callback_query(F.data.startswith('food_rating_'))
async def process_food_rating(callback_query: types.CallbackQuery, state: FSMContext):
    rating = callback_query.data.split('_')[2]
    await state.update_data(food_rating=rating)
    await state.set_state(RestorauntReview.cleanliness_rating)
    await callback_query.answer()

    kbforcleanrate = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=str(i), callback_data=f'cleanliness_rating_{i}') for i in range(1, 6)]
        ]
    )
    await callback_query.message.answer('Какую оценку вы поставите чистоте в нашей пиццерии?',
                                        reply_markup=kbforcleanrate)


@review_router.callback_query(F.data.startswith('cleanliness_rating_'))
async def process_cleanliness_rating(callback_query: types.CallbackQuery, state: FSMContext):
    rating = callback_query.data.split('_')[2]
    await state.update_data(cleanliness_rating=rating)
    await state.set_state(RestorauntReview.extra_comment)
    await callback_query.answer()
    await callback_query.message.answer('Есть ли какие-нибудь дополнения?')


@review_router.message(RestorauntReview.extra_comment)
async def process_extra_comment(message: types.Message, state: FSMContext):
    await state.update_data(extra_comment=message.text)
    reviewed_users.add(message.from_user.id)
    await state.clear()
    await message.answer("Спасибо за ваш отзыв!")

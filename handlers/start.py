from aiogram import Router, types
from aiogram.filters import Command


start_router = Router()
# counter_uniq_id = 0
# id_list = []
@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    # global counter_uniq_id
    # if message.from_user.id not in id_list:
    #     id_list.append(message.from_user.id)
    #     counter_uniq_id += 1
    name = message.from_user.first_name
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text = 'Наш сайт',
                    url = 'https://dodopizza.kg/bishkek'
                )
            ],
            [
                types.InlineKeyboardButton(
                    text= 'Наш IG',
                    url = 'https://www.instagram.com/dodopizzakg/'
                )
            ]
        ]
    )
    msg = f'Привет, {name}!. Вас приветствует пиццерия Dodo'
    await message.answer(msg,reply_markup=kb)
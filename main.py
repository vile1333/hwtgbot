import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import dotenv_values
import random

token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()
counter_uniq_id = 0
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    global counter_uniq_id
    id_list = []
    if message.from_user.id not in id_list:
        id_list.append(message.from_user.id)
        counter_uniq_id += 1
    name = message.from_user.first_name

    msg = f'Привет, {name}, наш бот обслуживает {counter_uniq_id} пользователя !'
    await message.answer(msg)

@dp.message(Command('myinfo'))
async def myinfo_handler(message: types.Message):
    id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username
    msg = f'Ваш id:{id}, Имя:{name}, username:{username}'
    await message.answer(msg)

@dp.message(Command('random'))
async def random_handler(message: types.Message):
    list_names = ['Айбек', 'Бектур', 'Игорь', 'Вася', 'Петя']
    choice = random.choice(list_names)
    await message.answer(choice)

@dp.message()
async def echo_handler(message: types.Message):
    # Обработчик сообщений
    await message.answer(message.text)

async def main():
    # Запуск бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


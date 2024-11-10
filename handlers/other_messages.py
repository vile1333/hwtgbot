from aiogram import Router, types
from aiogram.filters import Command


other_message = Router()

@other_message.message()
async def echo_handler(message: types.Message):
    # Обработчик сообщений
    await message.answer(message.text)
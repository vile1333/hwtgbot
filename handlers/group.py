from aiogram import Router, F , types
from aiogram.filters import Command

group_router = Router()

BadWords = ('дурак','тупой')

@group_router.message(Command("ban",prefix="!"))
async def ban_user(message: types.Message):
    if not message.reply_to_message:
        await message.answer("You need to reply to a message!")
    else:
        id_of_user = message.reply_to_message.from_user.id
        await message.bot.ban_chat_member(chat_id = message.chat.id, user_id=id_of_user)

@group_router.message(F.text)
async def check_bad_words(message: types.Message):
    txt = message.text.lower()
    for word in BadWords:
        if txt == word:
            userid = message.from_user.id
            await message.bot.ban_chat_member(chat_id=message.chat.id, user_id= userid )
            break


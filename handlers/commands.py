from aiogram import Router, types
from aiogram.filters import Command
import random


random_router = Router()
myinfo_router = Router()

@random_router.message(Command('random'))
async def random_handler(message: types.Message):
    list_of_dishes = ['images/borsch_with_recipe.jpg', 'images/kiev_cutlets_with_recipe.jpg',
                       'images/pizza_with_recipe.jpg',]
    list_of_captions = ['Ингредиенты: 2 средние свёклы, очищенные и натёртые 1 средняя картофелина, нарезанная кубиками'
                        '1 большая морковь, натёртая 1/2 маленькой капусты, нашинкованная 1 луковица, мелко нарезанная '
                        '2 зубчика чеснока, измельчённые 200 г говядины (по желанию), нарезанной кусочками '
                        '1 ст. ложка томатной пасты 6 стаканов воды или бульона Соль и перец по вкусу '
                        'Свежий укроп и петрушка для украшения Сметана для подачи', 'Ингредиенты: '
                        '2 куриные грудки 100 г сливочного масла (холодного)Свежая петрушка, мелко нарезанная'
                        '1 зубчик чеснока, измельчённый Соль и перец по вкусу 1 яйцо, взбитое'
                        'Мука и панировочные сухари для обваливания' ,'Ингредиенты: '
                        '250 г муки 150 мл тёплой воды 1 ч.л. сухих дрожжей 1/2 ч.л. соли '
                        '1 ст.л. оливкового масла 100 г томатного соуса 150 г тёртого сыра '
                        'Пепперони и свежий базилик для украшения']
    choice = random.choice(list_of_dishes)
    index = list_of_dishes.index(choice)
    photo = types.FSInputFile(choice)
    await message.answer_photo(photo,caption=list_of_captions[index])

@myinfo_router.message(Command('myinfo'))
async def myinfo_handler(message: types.Message):
        id = message.from_user.id
        name = message.from_user.first_name
        username = message.from_user.username
        msg = f'Ваш id:{id}, Имя:{name}, username:{username}'
        await message.answer(msg)
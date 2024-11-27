from aiogram import Router, F

from .start import start_router
from .dishes import dish_router
from .admin_book import admin_dish_router
from .random import random_router
from .picture import picture_router
from .my_info import myinfo_router
from .review_dialog import review_router
from .other_messages import other_message


private_router = Router()

private_router.include_router(random_router)
private_router.include_router(start_router)
private_router.include_router(myinfo_router)
private_router.include_router(picture_router)
private_router.include_router(review_router)
private_router.include_router(dish_router)
private_router.include_router(admin_dish_router)

private_router.include_router(other_message)

private_router.message.filter(F.chat.type == "private")


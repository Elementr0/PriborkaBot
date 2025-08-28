from aiogram.types import Message
from aiogram import Router, F

from config import ADMIN
from inlineKeyboars.inline_Keyboard.admin.adm_Lectures_menu import adm_Lectures_menu

router = Router()

@router.message(F.text=="Лекции")
async def txt_Lectures(message:Message):
    if str(message.from_user.id) in ADMIN:
        await message.answer("Админ меню:", reply_markup=adm_Lectures_menu)
    await message.answer(text="Выберите предмет:")
from aiogram.types import Message
from aiogram import Router, F

from config import ADMIN
from inlineKeyboars.inline_Button.admin.adm_get_subjects_keyboard import get_subjects_keyboard
from inlineKeyboars.inline_Keyboard.admin.adm_Lectures_menu import adm_Lectures_menu
from database.crud import is_admin

router = Router()


@router.message(F.text == "📚 Лекции")
async def txt_Lectures(message: Message):

    if  await is_admin(str(message.from_user.id)):
        await message.answer("Админ меню:", reply_markup=adm_Lectures_menu)

    # Добавлен await перед асинхронной функцией
    kb = await get_subjects_keyboard()

    if not kb:
        await message.answer("Нет доступных предметов")
        return

    await message.answer("Выбери предмет:", reply_markup=kb)
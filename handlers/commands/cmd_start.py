from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database.crud import set_user
from keyboards.keyboard.main_menu import main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("👋 Привет! Я твой бот-помошник по учебе!", reply_markup=main_menu)
    await set_user(message.from_user.id)

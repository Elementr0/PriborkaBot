from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.crud import get_subgroup, set_subgroup
from inlineKeyboars.inline_Keyboard.schedule import schedule_menu

router = Router()

@router.callback_query(F.data == "first_subgroup")
async def handle_monday_schedule(callback: CallbackQuery):
    await set_subgroup(int(callback.from_user.id), subgroup=1)
    await callback.message.answer(text="📅 Расписание:", reply_markup=schedule_menu)
    await callback.answer()
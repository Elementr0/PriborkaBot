from aiogram import Router, F
from aiogram.types import Message

from database.crud import check_tgid_exists
from inlineKeyboars.inline_Keyboard.schedule import schedule_menu
from inlineKeyboars.inline_Keyboard.subgroup import subgroup_menu

router = Router()

@router.message(F.text == "📅 Расписание")
async def show_schedule(message: Message):
    if await check_tgid_exists(int(message.from_user.id)) :
        await message.answer(text="📅 Расписание:", reply_markup=schedule_menu)
    else:
        await message.answer(text="Выбери свою подгруппу:", reply_markup=subgroup_menu)
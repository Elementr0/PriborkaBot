from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from FSMContexts.addLecture import AddLecture
from database.crud import add_lecture
from utils.utils_validation import is_valid_date

router = Router()


@router.message(AddLecture.waiting_for_date)
async def admin_date(message: Message, state: FSMContext):
    date = message.text.strip()
    if not is_valid_date(date):
        await message.answer("❌ Неверный формат даты! Используй DD-MM-YYYY (например: 01-09-2025)")
        return
    data = await state.get_data()
    subject = data["subject"]
    photos = data["photos"]
    for file_id in photos:
        await add_lecture(subject, date, file_id)
    await message.answer(f"✅ Лекции сохранены!\nПредмет: {subject}\nДата: {date}")
    await state.clear()
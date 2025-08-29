from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from FSMContexts.addLecture import AddLecture

router = Router()

@router.callback_query(AddLecture.waiting_for_subject, F.data.startswith("subject_"))
async def admin_subject(callback: CallbackQuery, state: FSMContext):
    subject = callback.data.replace("subject_", "")
    await state.update_data(subject=subject)
    await callback.message.answer("Введи дату лекции (формат: DD-MM-YYYY, например: 2025-09-01)")
    await state.set_state(AddLecture.waiting_for_date)
    await callback.answer()  # Добавляем ответ на callback
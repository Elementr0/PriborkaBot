from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from FSMContexts.addLecture import AddLecture
from database.crud import get_dates_for_subject
from inlineKeyboars.inline_Keyboard.dates import get_dates_keyboard

router = Router()

@router.callback_query(F.data.startswith("subject_"))
async def choose_subject(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == AddLecture.waiting_for_subject.state:
        # Не обрабатываем здесь, пусть обработает админский обработчик
        return

    subject = callback.data.replace("subject_", "")
    dates = await get_dates_for_subject(subject)
    if not dates:
        await callback.message.edit_text("Нет лекций по этому предмету")
        await callback.answer()
        return

    kb = get_dates_keyboard(subject, dates)
    await callback.message.edit_text(f"Выбери дату по предмету {subject}:", reply_markup=kb)
    await callback.answer()
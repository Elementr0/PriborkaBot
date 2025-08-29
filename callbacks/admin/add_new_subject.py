from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from FSMContexts.addLecture import AddLecture

router = Router()

@router.callback_query(AddLecture.waiting_for_subject, F.data == "add_new_subject")
async def start_add_subject_in_lecture(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введи название нового предмета:")
    await state.set_state(AddLecture.waiting_for_new_subject)  # Изменено состояние
    await callback.answer()  # Добавлен ответ на callback
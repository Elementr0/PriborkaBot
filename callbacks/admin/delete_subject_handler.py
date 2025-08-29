from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from FSMContexts.addSubject import ManageSubject
from database.crud import delete_subject

router = Router()


@router.callback_query(ManageSubject.waiting_for_subject_to_delete, F.data.startswith("subject_"))
async def delete_subject_handler(callback: CallbackQuery, state: FSMContext):
    subject = callback.data.replace("subject_", "")

    # Добавлен await перед асинхронной функцией
    success = await delete_subject(subject)

    if success:
        await callback.message.answer(f"✅ Предмет '{subject}' и все его лекции удалены!")
    else:
        await callback.message.answer("❌ Предмет не найден!")

    await state.clear()
    await callback.answer()  # Добавлен ответ на callback
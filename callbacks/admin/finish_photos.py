from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from FSMContexts.addLecture import AddLecture
from inlineKeyboars.inline_Button.admin.adm_get_subjects_keyboard import get_subjects_keyboard

router = Router()


@router.callback_query(AddLecture.waiting_for_photos, F.data == "finish_upload")
async def finish_photos(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if "photos" not in data or not data["photos"]:
        await callback.message.answer("❌ Ты не загрузил ни одной фотографии!")
        await callback.answer()  # Добавляем ответ на callback
        return

    # Добавляем await перед асинхронной функцией
    kb = await get_subjects_keyboard(add_new_subject_option=True)

    if not kb:
        await callback.message.answer("Нет доступных предметов. Создай новый предмет:")
        await state.set_state(AddLecture.waiting_for_new_subject)
        await callback.answer()
        return

    await callback.message.answer("Выбери предмет или добавь новый:", reply_markup=kb)
    await state.set_state(AddLecture.waiting_for_subject)
    await callback.answer()  # Завершаем callback
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram.types import CallbackQuery
from aiogram import F

from FSMContexts.addLecture import AddLecture
from database.crud import add_subject
from inlineKeyboars.inline_Button.admin.adm_get_subjects_keyboard import get_subjects_keyboard

router = Router()

@router.callback_query(AddLecture.waiting_for_subject, F.data.startswith("subject_"))
async def choose_existing_subject(callback: CallbackQuery, state: FSMContext):
    subject_id = callback.data.split("_", 1)[1]
    await state.update_data(subject=subject_id)
    await callback.message.answer(
        "Выбран существующий предмет! Введи дату лекции (формат: DD-MM-YYYY, например: 01-09-2025)"
    )
    await state.set_state(AddLecture.waiting_for_date)
    await callback.answer()


@router.message(AddLecture.waiting_for_new_subject)
async def add_subject_in_lecture(message: Message, state: FSMContext):
    subject_name = message.text.strip()

    if not subject_name:
        await message.answer("❌ Название предмета не может быть пустым!")
        return

    # Добавляем await перед асинхронной функцией
    success = await add_subject(subject_name)

    if not success:
        await message.answer("❌ Предмет уже существует! Выбери другой или используй существующий:")
        # Добавляем await перед асинхронной функцией
        kb = await get_subjects_keyboard(add_new_subject_option=True)
        await message.answer("Выбери предмет:", reply_markup=kb)
        await state.set_state(AddLecture.waiting_for_subject)
        return

    await state.update_data(subject=subject_name)
    await message.answer(
        f"✅ Предмет '{subject_name}' добавлен! Введи дату лекции (формат: DD-MM-YYYY, например: 01-09-2025)")
    await state.set_state(AddLecture.waiting_for_date)
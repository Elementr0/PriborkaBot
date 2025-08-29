from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from database.crud import is_admin

from FSMContexts.addSubject import ManageSubject
from config import ADMIN
from inlineKeyboars.inline_Button.admin.adm_get_subjects_keyboard import get_subjects_keyboard

router = Router()


@router.callback_query(F.data == "delete_subject")
async def start_delete_subject(callback: CallbackQuery, state: FSMContext):
    # Проверяем, что пользователь является администратором
    if not await is_admin(str(callback.from_user.id)):  # Исправлено сравнение
        await callback.answer("❌ Нет доступа!")  # Добавлен ответ
        return

    # Добавляем await перед асинхронной функцией
    kb = await get_subjects_keyboard()

    if not kb:
        await callback.message.answer("❌ Нет предметов для удаления!")
        await callback.answer()  # Добавляем ответ на callback
        return

    await callback.message.answer("Выбери предмет для удаления:", reply_markup=kb)
    await state.set_state(ManageSubject.waiting_for_subject_to_delete)
    await callback.answer()  # Завершаем callback запрос
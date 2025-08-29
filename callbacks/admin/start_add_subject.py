from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from FSMContexts.addSubject import ManageSubject
from config import ADMIN
from database.crud import is_admin

router = Router()


@router.callback_query(F.data == "add_subject")
async def start_add_subject(callback: CallbackQuery, state: FSMContext):
    if not await is_admin(str(callback.from_user.id)): # Исправлено сравнение
        await callback.answer("❌ Нет доступа!")  # Добавлен ответ
        return

    await callback.message.answer("Введи название нового предмета:")
    await state.set_state(ManageSubject.waiting_for_subject_name)
    await callback.answer()  # Добавлен ответ на callback
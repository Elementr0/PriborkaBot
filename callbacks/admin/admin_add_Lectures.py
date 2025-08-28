from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from inlineKeyboars.inline_Keyboard.admin.adm_finish_uploadPhoto_menu import adm_finish_uploadPhoto_menu

router = Router()

@router.callback_query(F.data == "admin_add_Lectures")
async def admin_add_Lectures(callback:CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer("Отправь фото лекции (можно несколько подряд). Когда закончишь — нажми ✅ Завершить загрузку", reply_markup=adm_finish_uploadPhoto_menu)
    await callback.answer()
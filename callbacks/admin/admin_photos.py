from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from FSMContexts.addLecture import AddLecture

router = Router()

@router.message(AddLecture.waiting_for_photos, F.photo)
async def admin_photos(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    data = await state.get_data()
    photos = data.get("photos", [])
    photos.append(file_id)
    await state.update_data(photos=photos)
    await message.answer("Фото добавлено ✅ (можно ещё)")
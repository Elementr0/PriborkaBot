from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto

from database.crud import get_photos_for_subject_date

router = Router()


@router.callback_query(F.data.startswith("date_"))
async def choose_date(callback: CallbackQuery):
    _, subject, date = callback.data.split("_", 2)
    photos = await get_photos_for_subject_date(subject, date)

    if not photos:
        await callback.message.edit_text("Лекций нет")
        await callback.answer()  # Завершаем callback
        return

    # Отвечаем на callback чтобы убрать "часики" у кнопки
    await callback.answer()

    if len(photos) > 1:
        media_group = [InputMediaPhoto(media=photo) for photo in photos]
        await callback.message.answer_media_group(media_group)
    else:
        await callback.message.answer_photo(photos[0])
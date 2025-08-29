from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.crud import  get_subjects


async def get_subjects_keyboard(add_new_subject_option=False):  # Добавлен async
    subjects = await get_subjects()  # Добавлен await
    if not subjects and not add_new_subject_option:
        return None
    keyboard = [
        [InlineKeyboardButton(text=f"📖 {s.name}", callback_data=f"subject_{s.name}")]
        for s in subjects
    ]
    if add_new_subject_option:
        keyboard.append([InlineKeyboardButton(text="➕ Добавить новый предмет", callback_data="add_new_subject")],
                        [InlineKeyboardButton(text="➕ Добавить предмет", callback_data="add_subject")],
                        )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
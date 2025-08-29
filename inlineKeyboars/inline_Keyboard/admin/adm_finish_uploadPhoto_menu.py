from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from inlineKeyboars.inline_Button.admin.adm_finish_uploadPhoto import adm_finish_uploadPhoto

adm_finish_uploadPhoto_menu=InlineKeyboardMarkup(
    inline_keyboard=[
        [adm_finish_uploadPhoto],
        # [InlineKeyboardButton(text="➕ Добавить предмет", callback_data="add_subject")],
        # [InlineKeyboardButton(text="➖ Удалить предмет", callback_data="delete_subject")]
    ]
)
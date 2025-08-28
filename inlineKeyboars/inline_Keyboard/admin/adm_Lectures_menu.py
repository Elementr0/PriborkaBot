from aiogram.types import InlineKeyboardMarkup

from inlineKeyboars.inline_Button.admin.adm_inbtn_add_Lectures import adm_inbtn_add_Lectures

adm_Lectures_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [adm_inbtn_add_Lectures]
    ]
)
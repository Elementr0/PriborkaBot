from aiogram.types import InlineKeyboardMarkup

from inlineKeyboars.inline_Button.inl_schedule_monday import inl_schedule_monday
from inlineKeyboars.inline_Button.inl_schedule_tuesday import inl_schedule_tuesday

schedule_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [inl_schedule_monday, inl_schedule_tuesday]
    ],
)
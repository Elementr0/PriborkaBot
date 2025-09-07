from aiogram.types import InlineKeyboardMarkup

from inlineKeyboars.inline_Button.inl_schedule_friday import inl_schedule_friday
from inlineKeyboars.inline_Button.inl_schedule_monday import inl_schedule_monday
from inlineKeyboars.inline_Button.inl_schedule_saturday import inl_schedule_saturday
from inlineKeyboars.inline_Button.inl_schedule_thursday import inl_schedule_thursday
from inlineKeyboars.inline_Button.inl_schedule_tuesday import inl_schedule_tuesday

from aiogram.types import InlineKeyboardButton

from inlineKeyboars.inline_Button.inl_schedule_wednesday import inl_schedule_wednesday

schedule_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [inl_schedule_monday, inl_schedule_tuesday, inl_schedule_wednesday, inl_schedule_thursday, inl_schedule_friday, inl_schedule_saturday]
    ],
)
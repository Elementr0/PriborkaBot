from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

subgroup_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Первая", callback_data="first_subgroup"),
         InlineKeyboardButton(text="Вторая", callback_data="second_subgroup")]
    ],
)

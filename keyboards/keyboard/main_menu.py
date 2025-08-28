from aiogram.types import ReplyKeyboardMarkup

from keyboards.button.btn_Lectures import btn_Lectures

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [btn_Lectures]
    ],
    resize_keyboard= True
)
from aiogram.types import ReplyKeyboardMarkup

from keyboards.button.btn_Lectures import btn_Lectures
from keyboards.button.btn_teacher import btn_teacher

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [btn_Lectures],
        [btn_teacher]
    ],
    resize_keyboard= True
)
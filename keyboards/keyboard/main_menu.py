from aiogram.types import ReplyKeyboardMarkup

from keyboards.button.btn_Schedule import btn_Schedule
from keyboards.button.btn_Lectures import btn_Lectures
from keyboards.button.btn_teacher import btn_teacher

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [btn_Lectures],
        [btn_teacher],
        [btn_Schedule]
    ],
    resize_keyboard= True
)
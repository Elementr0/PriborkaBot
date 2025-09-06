# Технические импорты
import asyncio

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import handlers
from callbacks.admin import (
    finish_photos, admin_subject, admin_date, add_new_subject, add_subject_in_lecture,
    start_add_subject, add_subject_handler, start_delete_subject, delete_subject_handler,
    admin_add_Lectures, admin_photos, handle_monday_schedule
)
from callbacks import choose_subject, choose_date, handle_second_subgroup, handle_first_subgroup
from config import BOT_TOKEN

from aiogram import Bot, Dispatcher

from database.crud import create_tables, add_subject, get_teacher, set_teacher, fill_schedule, get_day, get_day_full
from handlers.commands import cmd_start
from handlers.text import txt_Lectures, txt_Teachers, txt_schedule
from handlers.commands import cmd_add_admin

async def main():
    await create_tables()
    bot = Bot(token=BOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML)
              )
    dp = Dispatcher()

    # Коллбэки (сначала админские, потом общие)
    dp.include_router(cmd_add_admin.router)
    dp.include_router(admin_add_Lectures.router)
    dp.include_router(admin_photos.router)
    dp.include_router(finish_photos.router)
    dp.include_router(choose_date.router)
    dp.include_router(add_subject_in_lecture.router)  # Важно: до choose_subject!
    dp.include_router(choose_subject.router)
    dp.include_router(admin_subject.router)
    dp.include_router(admin_date.router)
    dp.include_router(add_new_subject.router)
    dp.include_router(start_add_subject.router)
    dp.include_router(add_subject_handler.router)
    dp.include_router(start_delete_subject.router)
    dp.include_router(delete_subject_handler.router)
    dp.include_router(handle_monday_schedule.router)
    dp.include_router(handle_first_subgroup.router)
    dp.include_router(handle_second_subgroup.router)

    # Команды
    dp.include_router(cmd_start.router)

    # Текст
    dp.include_router(txt_Lectures.router)
    dp.include_router(txt_Teachers.router)
    dp.include_router(txt_schedule.router)


    data_up_week = [
    # Понедельник
    {
        "week": "up",
        "day": "Понедельник",
        "hour": "8:00-9:35",
        "subgroup": 2,
        "subject": "Иностранный язык для деловойкоммуникации (В)",
        "classroom": "815",
        "teacher": "Осипова О. С"
    },
    {
        "week": "up",
        "day": "Понедельник",
        "hour": "9:50-11:25",
        "subgroup": 2,
        "subject": "Ультразвуковые методы неразрушающего контроля (лаб)",
        "classroom": "709",
        "teacher": "Мараховский М. А."
    },
    {
        "week": "up",
        "day": "Понедельник",
        "hour": "11:55-13:30",
        "subgroup": 1 ,
        "subject": "Компьютерные технологии в приборостростроении(лек)",
        "classroom": "Ключников С. Н.",
        "teacher": "711"
    },
    {
        "week": "up",
        "day": "Понедельник",
        "hour": "11:55-13:30",
        "subgroup": 2,
        "subject": "Компьютерные технологии в приборостростроении(лек)",
        "classroom": "Ключников С. Н.",
        "teacher": "711"
    },
    {
        "week": "up",
        "day": "Понедельник",
        "hour": "13:45-15:20",
        "subgroup": 1,
        "subject": "Ультразвуковые методы неразрушающего контроля (лаб)",
        "classroom": "Мароховский М. А",
        "teacher": "103"
    },
    # Вторник
        {
            "week": "up",
            "day": "Вторник",
            "hour": "8:00-17:35",
            "subgroup": 1,
            "subject": "Спец. Подготовка",
            "classroom": "-",
            "teacher": "-"
        },
        {
            "week": "up",
            "day": "Вторник",
            "hour": "8:00-17:35",
            "subgroup": 2,
            "subject": "Спец. Подготовка",
            "classroom": "-",
            "teacher": "-"
        },
        #Среда
        {
            "week": "up",
            "day": "Среда",
            "hour": "9:50-11:25",
            "subgroup": 1,
            "subject": "Пьезокерамические преобразователи и измерительные тракты (лаб.)",
            "classroom": "709а",
            "teacher": "Соколов М. В."
        },
        {
            "week": "up",
            "day": "Среда",
            "hour": "11:55-13:30",
            "subgroup": 1,
            "subject": "Ультразвуковые методы неразрушающего контроля (лекц.)",
            "classroom": "711",
            "teacher": "Мараховский М. А"
        },

]
    await fill_schedule(data_up_week)
    print(await get_day_full(week="up", day="Понедельник", subgroup=2))

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
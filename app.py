# Технические импорты
import asyncio

import handlers
from callbacks.admin import (
    finish_photos, admin_subject, admin_date, add_new_subject, add_subject_in_lecture,
    start_add_subject, add_subject_handler, start_delete_subject, delete_subject_handler,
    admin_add_Lectures, admin_photos
)
from callbacks import choose_subject, choose_date
from config import BOT_TOKEN

from aiogram import Bot, Dispatcher

from database.crud import create_tables, add_subject
from handlers.commands import cmd_start
from handlers.text import txt_Lectures
from handlers.commands import cmd_add_admin

async def main():
    await create_tables()
    bot = Bot(token=BOT_TOKEN)
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

    # Команды
    dp.include_router(cmd_start.router)

    # Текст
    dp.include_router(txt_Lectures.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
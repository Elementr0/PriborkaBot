#Технические импорты
import asyncio

import handlers
#Конфигурационные импорты
from config import BOT_TOKEN

#Ипорты фрейворка
from aiogram import Bot, Dispatcher

#Программные импорты
from database.crud import create_tables
from handlers.commands import cmd_start
from handlers.text import txt_Lectures
from callbacks.admin import admin_add_Lectures

async def main():
    await create_tables()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    #Коллбэки
    dp.include_router(admin_add_Lectures.router)

    #Команды
    dp.include_router(cmd_start.router)

    #Текст
    dp.include_router(txt_Lectures.router)

    await dp.start_polling(bot)

    
    
if __name__ == "__main__":
    asyncio.run(main())
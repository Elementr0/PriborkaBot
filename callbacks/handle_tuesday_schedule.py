from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.crud import get_day, get_subgroup
from inlineKeyboars.inline_Keyboard.schedule import schedule_menu

import datetime


router = Router()


@router.callback_query(F.data == "schedule_monday")
async def handle_tuesday_schedule(callback: CallbackQuery):
    try:
        date = datetime.date.today().isocalendar()[1] #Узнаём номер недели
        if (date % 2) == 0: #чётная неделя вернхяя нечетная нижняя
            week = "up"
        else:
            week = "down"
        subgroup = await get_subgroup(callback.from_user.id)
        schedule = await get_day(week, "Понедельник", subgroup)

        response_text = "📅 <b>Расписание на понедельник:</b>\n\n"

        if not schedule:
            response_text += "❌ Занятий не найдено"
        else:
            # Функция для преобразования времени в минуты для сортировки
            def time_to_minutes(time_str):
                try:
                    # Берем начало временного интервала (8:00 из "8:00-9:35")
                    start_time = time_str.split('-')[0].strip()
                    hours, minutes = map(int, start_time.split(':'))
                    return hours * 60 + minutes
                except (IndexError, ValueError):
                    return 0  # Если формат неправильный, ставим в начало

            # Сортируем расписание по начальному времени
            sorted_schedule = sorted(schedule, key=lambda x: time_to_minutes(x.get('hour', '')))

            for i, lesson in enumerate(sorted_schedule, 1):
                hour = lesson.get('hour', '⏰ Время не указано')
                subject = lesson.get('subject', '📖 Предмет не указан')
                classroom = lesson.get('classroom', '🏫 Аудитория не указана')
                teacher = lesson.get('teacher', '👨‍🏫 Преподаватель не указан')

                response_text += (
                    f"⏰Время: <b>{hour}</b>\n"
                    f"📖Предмет: {subject}\n"
                    f"🏫Аудитория: {classroom}\n"
                    f"👨‍🏫Преподователь: {teacher}\n"
                )

                # Добавляем разделитель между предметами, кроме последнего
                if i < len(sorted_schedule):
                    response_text += "\n" + "─" * 30 + "\n\n"

        await callback.message.edit_text(
            text=response_text,
            reply_markup=schedule_menu,
            parse_mode="HTML"
        )
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text("❌ Ошибка загрузки расписания")
        await callback.answer()
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from database.crud import get_day, get_subgroup
from inlineKeyboars.inline_Keyboard.schedule import schedule_menu
import datetime

router = Router()


def get_week_switch_keyboard(day: str, current_week: str):
    """Клавиатура для переключения недель"""
    other_week = "down" if current_week == "up" else "up"
    week_text = "Нижняя неделя" if other_week == "down" else "Верхняя неделя"

    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f"🔄 {week_text}",
                callback_data=f"schedule_{day}_{other_week}"
            )
        ],
        [
            InlineKeyboardButton(
                text="← Назад к дням",
                callback_data="back_to_schedule"
            )
        ]
    ])


def get_current_week():
    """Определяет текущую неделю"""
    week_number = datetime.date.today().isocalendar()[1]
    return "up" if (week_number % 2) == 0 else "down"


# Обработчики для всех дней недели
@router.callback_query(F.data == "schedule_monday")
async def handle_monday_schedule(callback: CallbackQuery):
    try:
        current_week = get_current_week()
        await show_schedule(callback, "Понедельник", current_week)
    except Exception as e:
        await callback.message.edit_text("❌ Ошибка загрузки расписания")
        await callback.answer()


@router.callback_query(F.data == "schedule_tuesday")
async def handle_tuesday_schedule(callback: CallbackQuery):
    try:
        current_week = get_current_week()
        await show_schedule(callback, "Вторник", current_week)
    except Exception as e:
        await callback.message.edit_text("❌ Ошибка загрузки расписания")
        await callback.answer()


@router.callback_query(F.data == "schedule_wednesday")
async def handle_wednesday_schedule(callback: CallbackQuery):
    try:
        current_week = get_current_week()
        await show_schedule(callback, "Среда", current_week)
    except Exception as e:
        await callback.message.edit_text("❌ Ошибка загрузки расписания")
        await callback.answer()


@router.callback_query(F.data == "schedule_thursday")
async def handle_thursday_schedule(callback: CallbackQuery):
    try:
        current_week = get_current_week()
        await show_schedule(callback, "Четверг", current_week)
    except Exception as e:
        await callback.message.edit_text("❌ Ошибка загрузки расписания")
        await callback.answer()


@router.callback_query(F.data == "schedule_friday")
async def handle_friday_schedule(callback: CallbackQuery):
    try:
        current_week = get_current_week()
        await show_schedule(callback, "Пятница", current_week)
    except Exception as e:
        await callback.message.edit_text("❌ Ошибка загрузки расписания")
        await callback.answer()


@router.callback_query(F.data == "schedule_saturday")
async def handle_saturday_schedule(callback: CallbackQuery):
    try:
        current_week = get_current_week()
        await show_schedule(callback, "Суббота", current_week)
    except Exception as e:
        await callback.message.edit_text("❌ Ошибка загрузки расписания")
        await callback.answer()


@router.callback_query(F.data.startswith("schedule_"))
async def handle_week_switch(callback: CallbackQuery):
    """Обработчик переключения недель"""
    try:
        data_parts = callback.data.split('_')
        if len(data_parts) >= 3:
            day_name = data_parts[1]  # Название дня (monday, tuesday и т.д.)
            week_type = data_parts[2]  # up или down

            # Преобразуем английское название в русское
            days_map = {
                "monday": "Понедельник",
                "tuesday": "Вторник",
                "wednesday": "Среда",
                "thursday": "Четверг",
                "friday": "Пятница",
                "saturday": "Суббота"
            }

            russian_day = days_map.get(day_name, "Понедельник")
            await show_schedule(callback, russian_day, week_type)

    except Exception as e:
        await callback.message.edit_text("❌ Ошибка загрузки расписания")
        await callback.answer()


@router.callback_query(F.data == "back_to_schedule")
async def back_to_schedule(callback: CallbackQuery):
    """Возврат к выбору дней"""
    await callback.message.edit_text(
        text="📅 Выберите день недели:",
        reply_markup=schedule_menu
    )
    await callback.answer()


async def show_schedule(callback: CallbackQuery, day: str, week: str):
    """Показывает расписание"""
    try:
        subgroup = await get_subgroup(callback.from_user.id)
        schedule = await get_day(week, day, subgroup)

        week_text = "верхняя" if week == "up" else "нижняя"
        response_text = f"📅 <b>Расписание на {day.lower()} ({week_text} неделя):</b>\n\n"

        if not schedule:
            response_text += "❌ Занятий не найдено"
        else:
            # Сортируем расписание по времени
            def time_to_minutes(time_str):
                try:
                    start_time = time_str.split('-')[0].strip()
                    hours, minutes = map(int, start_time.split(':'))
                    return hours * 60 + minutes
                except:
                    return 0

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

                if i < len(sorted_schedule):
                    response_text += "\n" + "─" * 30 + "\n\n"

        # Получаем клавиатуру для переключения недель
        # Используем английское название дня для callback_data
        eng_days_map = {
            "Понедельник": "monday",
            "Вторник": "tuesday",
            "Среда": "wednesday",
            "Четверг": "thursday",
            "Пятница": "friday",
            "Суббота": "saturday"
        }

        eng_day = eng_days_map.get(day, "monday")
        keyboard = get_week_switch_keyboard(eng_day, week)

        await callback.message.edit_text(
            text=response_text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        await callback.answer()

    except Exception as e:
        await callback.message.edit_text("❌ Ошибка загрузки расписания")
        await callback.answer()
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from database.crud import get_day, get_subgroup
from inlineKeyboars.inline_Keyboard.schedule import schedule_menu

router = Router()


@router.callback_query(F.data == "schedule_monday")
async def handle_monday_schedule(callback: CallbackQuery):

    try:
        subgroup = await get_subgroup(callback.from_user.id)

        schedule = await get_day("up", "Понедельник", subgroup)

        response_text = "📅 <b>Расписание на понедельник:</b>\n\n"

        if not schedule:
            response_text += "❌ Занятий не найдено"
        else:
            for i, lesson in enumerate(schedule, 1):
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
                if i < len(schedule):
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
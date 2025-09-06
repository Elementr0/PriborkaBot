from aiogram import Router, F
from aiogram.types import Message

from database.crud import get_teacher

router = Router()

@router.message(F.text == "👨‍🏫 Преподы")
async def show_teachers(message: Message):
    try:
        # Получаем список преподавателей
        teachers_list = await get_teacher()

        if not teachers_list:
            await message.answer("📭 Список преподавателей пуст")
            return

        # Формируем красивое сообщение
        text = "👨‍🏫 <b>Список преподавателей</b>\n\n"

        for teacher in teachers_list:
            # Извлекаем данные из словаря
            name = teacher.get('teacher', 'Не указано')
            mood = teacher.get('mood', 'Не указано')
            subject = teacher.get('subject', 'Не указано')

            # Добавляем эмодзи в зависимости от настроения
            mood_emoji = {
                'хорошее': '😊',
                'плохое': '😠',
                'нейтральное': '😐',
                'отличное': '😎',
                'грустное': '😢'
            }.get(mood.lower(), '❓')

            text += f"• <b>{name}</b>\n"
            text += f"  📚 <i>Предмет:</i> {subject}\n"
            text += f"  {mood_emoji} <i>Настроение:</i> {mood}\n\n"

        text += f"<i>Всего преподавателей: {len(teachers_list)}</i>"

        await message.answer(text)

    except Exception as e:
        await message.answer("❌ Произошла ошибка при получении данных")
        print(f"Error: {e}")

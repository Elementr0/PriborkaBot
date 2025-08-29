from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from FSMContexts.addSubject import ManageSubject
from database.crud import add_subject

router = Router()  # Добавлены скобки


@router.message(ManageSubject.waiting_for_subject_name)
async def add_subject_handler(message: Message, state: FSMContext):
    subject_name = message.text.strip()

    if not subject_name:
        await message.answer("❌ Название предмета не может быть пустым!")
        return

    # Добавлен await перед асинхронной функцией
    success = await add_subject(subject_name)

    if success:
        await message.answer(f"✅ Предмет '{subject_name}' добавлен!")
    else:
        await message.answer("❌ Предмет уже существует!")

    await state.clear()
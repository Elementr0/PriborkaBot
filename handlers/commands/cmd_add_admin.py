from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import ADMIN
from database.crud import add_admin, is_admin

SUPER_ADMIN_ID = str(ADMIN[0])  # Замените на свой Telegram ID

router = Router()

class AddAdminFSM(StatesGroup):
    waiting_for_admin_id = State()

@router.message(Command("addadmin"))
async def add_admin_command(message: Message, state: FSMContext):
    print(SUPER_ADMIN_ID, ADMIN)
    if str(message.from_user.id) != SUPER_ADMIN_ID:
        await message.answer("Нет доступа.")
        return
    await message.answer("Отправьте ID пользователя, которого хотите сделать админом.")
    await state.set_state(AddAdminFSM.waiting_for_admin_id)

@router.message(AddAdminFSM.waiting_for_admin_id)
async def process_admin_id(message: Message, state: FSMContext):
    new_admin_id = message.text.strip()
    if await is_admin(new_admin_id):
        await message.answer("Этот пользователь уже админ.")
    else:
        await add_admin(new_admin_id)
        await message.answer(f"Пользователь {new_admin_id} теперь админ.")
    await state.clear()
from aiogram.fsm.state import State, StatesGroup


class AddLecture(StatesGroup):
    waiting_for_photo = State()
    waiting_for_suject = State()
    waiting_for_date = State()
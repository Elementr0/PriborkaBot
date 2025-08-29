from aiogram.fsm.state import State, StatesGroup


class AddLecture(StatesGroup):
    waiting_for_photos = State()
    waiting_for_subject = State()
    waiting_for_new_subject = State()
    waiting_for_date = State()
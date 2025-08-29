from aiogram.fsm.state import State, StatesGroup

class ManageSubject(StatesGroup):
    waiting_for_subject_name = State()
    waiting_for_subject_to_delete = State()
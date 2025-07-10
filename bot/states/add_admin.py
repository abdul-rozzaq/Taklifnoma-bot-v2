from aiogram.fsm.state import StatesGroup, State


class AddAdminState(StatesGroup):
    waiting_for_forward_message = State()
    waiting_for_confirmation = State()

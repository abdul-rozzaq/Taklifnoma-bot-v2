from aiogram.fsm.state import StatesGroup, State


class AchievementState(StatesGroup):
    waiting_for_achievement = State()

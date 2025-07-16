from aiogram.fsm.state import StatesGroup, State


# Состояние курса
class CourseState(StatesGroup):
    course = State()
    price = State()
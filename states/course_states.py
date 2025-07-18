from aiogram.fsm.state import StatesGroup, State


# Состояние курса
class CourseState(StatesGroup):
    course = State()
    price = State()


# Состояние оплаты
class PaymentsState(StatesGroup):
    '''
    pay_token = State()
    pay_sum = State()
    pay_bool = State()
    '''
    pay_token = State()
    pay_sum = State()
    pay_plan = State()
    pay_kb = State()
    pay_bool = State()

# Состояния для снятия реф денег
class TakeOffManyState(StatesGroup):
    """
    telegram_id = State()
    take_sum = State()
    take_bank = State()
    take_number = State()
    take_bool = State()
    """
    telegram_id = State()
    take_sum = State()
    take_bank = State()
    take_number = State()
    take_text = State()
    take_bool = State()
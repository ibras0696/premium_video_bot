from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

# Функции с БД
from database import CrudeUser


router = Router()


# Обработка старта через реферальную ссылку
@router.message(CommandStart(deep_link=True))
async def start_cmd(message: Message, state: FSMContext, command: CommandStart):
    # Чистка состояний
    await state.clear()

    # Проверка передачи реферального кода
    ref_id = command.args
    try:
        if ref_id:
            r_d = int(ref_id)
            # Берем реферальный код в случае присутствия
            await message.answer(f'Аргс: {ref_id}')
            # Добавляем в Базу
            await CrudeUser().add_user(telegram_id=message.from_user.id,
                                       user_name=message.from_user.username,
                                       referral_id=r_d)
            await message.answer('Привет <Видео>')
    # Если ведены доп параметры
    except ValueError:
        pass
    except Exception as ex:
        print(f'Ошибка: {ex}')


# Обработка обычного старта
@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    # Очистка состояний
    await state.clear()

    await message.answer('Привету')
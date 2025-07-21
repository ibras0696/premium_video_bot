from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import start_kb, ref_and_course_kb, course_kb, profile_kb, refer_kb
from utils import message_texts
from static.start_video_path import get_start_mov_file

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
            # Добавляем в Базу
            await CrudeUser().add_user(telegram_id=message.from_user.id,
                                       user_name=message.from_user.username,
                                       referral_id=r_d)
            # Отправляем сообщение с реферальной ссылкой
            await message.answer_video(message_texts.start_text, video=get_start_mov_file(), reply_markup=start_kb)
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
    # Добавляем в Базу
    await CrudeUser().add_user(telegram_id=message.from_user.id,
                               user_name=message.from_user.username)

    await message.answer_video(message_texts.start_text, video=get_start_mov_file(), reply_markup=start_kb)


@router.callback_query(F.data == 'start')
async def start_query(call_back: CallbackQuery):
    await call_back.message.edit_text(message_texts.ref_and_course_text, reply_markup=ref_and_course_kb)

# Обработка кнопки реф ссылки
@router.callback_query(F.data.startswith('get_start_'))
async def get_start_cmd(call_back: CallbackQuery):
    user_id = call_back.message.chat.id
    match call_back.data:
        case 'get_start_course':
            await call_back.message.edit_text(message_texts.course_text, reply_markup=course_kb)
        case 'get_start_profile':
            await call_back.message.edit_text(text=await message_texts.get_profile_text(user_id), reply_markup=profile_kb)
        case 'get_start_ref':
            await call_back.message.edit_text(await message_texts.refer_id_text(telegram_id=user_id), reply_markup=refer_kb(take=True))
        case _:
            pass

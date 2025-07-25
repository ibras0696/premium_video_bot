from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import CrudeUser
from keyboards import ref_and_course_kb, refer_kb
from states import TakeOffManyState
from utils import message_texts
from utils.message_texts import pay_take_text

router = Router()


@router.callback_query(F.data.startswith('profile_'))
async def profile_cmd(call_back: CallbackQuery):
    # Удаление мигающих кнопок
    await call_back.answer()

    match call_back.data:
        # case 'profile_take':
        #     await call_back.message.answer('Пока не готово')
        case 'profile_back':
            await call_back.message.edit_text(message_texts.ref_and_course_text, reply_markup=ref_and_course_kb)


@router.callback_query(F.data.startswith('ref_'))
async def refer_info_cmd(call_back: CallbackQuery, state: FSMContext):
    # Удаление мигающих кнопок
    await call_back.answer()

    user_id = call_back.message.chat.id
    match call_back.data:
        case 'ref_take':
            user = await CrudeUser().get_user(user_id)
            if 500 <= user.balance:
                await call_back.message.edit_text(text=message_texts.take_of_text, reply_markup=refer_kb())
                await state.set_state(TakeOffManyState.telegram_id)
            else:
                await call_back.message.edit_text(text=message_texts.warning_take_off_text, reply_markup=ref_and_course_kb)
        case 'ref_back':
            await call_back.message.edit_text(message_texts.ref_and_course_text, reply_markup=ref_and_course_kb)
        case _:
            pass
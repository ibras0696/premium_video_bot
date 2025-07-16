from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import ref_and_course_kb, refer_kb
from utils import message_texts
from utils.message_texts import pay_take_text

router = Router()


@router.callback_query(F.data.startswith('profile_'))
async def profile_cmd(call_back: CallbackQuery):
    match call_back.data:
        # case 'profile_take':
        #     await call_back.message.answer('Пока не готово')
        case 'profile_back':
            await call_back.message.edit_text(message_texts.ref_and_course_text, reply_markup=ref_and_course_kb)


@router.callback_query(F.data.startswith('ref_'))
async def refer_info_cmd(call_back: CallbackQuery):
    user_id = call_back.message.chat.id
    match call_back.data:
        case 'ref_take':
            await call_back.message.edit_text(text=pay_take_text, reply_markup=refer_kb())
        case 'ref_back':
            await call_back.message.edit_text(message_texts.ref_and_course_text, reply_markup=ref_and_course_kb)
        case _:
            pass
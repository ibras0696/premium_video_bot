from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import pay_course_kb, ref_and_course_kb
from states import CourseState
from utils import message_texts

router = Router()


@router.callback_query(F.data.startswith('course_'))
async def course_cmd(call_back: CallbackQuery, state: FSMContext):
    data = call_back.data.replace('course_', '')

    if data in ['base', 'advanced', 'exclusive', 'all']:
        await state.set_state(CourseState.course)
        await state.update_data(course=data)

    match data:
        case 'base':
            await call_back.message.edit_text(text=message_texts.base_course_text, reply_markup=pay_course_kb)
        case 'advanced':
            await call_back.message.edit_text(text=message_texts.advanced_course_text, reply_markup=pay_course_kb)
        case 'exclusive':
            await call_back.message.edit_text(text=message_texts.exclusive_course_text, reply_markup=pay_course_kb)
        case 'all':
            await call_back.message.edit_text(text=message_texts.all_course_text, reply_markup=pay_course_kb)
        case 'back':
            await call_back.message.edit_text(message_texts.ref_and_course_text, reply_markup=ref_and_course_kb)
        case _:
            pass

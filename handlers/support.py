from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from keyboards import support_kb, ref_and_course_kb
from utils import message_texts

router = Router()


@router.callback_query(F.data.startswith('support_'))
async def support_back_cmd(call_back: CallbackQuery):
    await call_back.message.edit_text(message_texts.ref_and_course_text, reply_markup=ref_and_course_kb)
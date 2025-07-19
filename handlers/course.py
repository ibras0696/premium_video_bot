from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import Subscriptions
from keyboards import pay_course_kb, ref_and_course_kb

from states import PaymentsState
from utils import message_texts
from services import create_payment

router = Router()


@router.callback_query(F.data.startswith('course_'))
async def course_cmd(call_back: CallbackQuery, state: FSMContext):
    kb = None

    data = call_back.data.replace('course_', '')

    if data in ['all', 'exclusive', 'advanced', 'base']:
        #  Список для получение цен для тарифов
        plans_price = Subscriptions.get_price_plans().get(data, 'base')
        # Список для получения название тарифов
        plans_info = Subscriptions.get_plans().get(data, 'base')
        # Создание платежа
        payment = create_payment(
            amount=plans_price,
            telegram_id=call_back.message.chat.id,
            description=f'Покупка {plans_info}а',
        )
        # Создание клавиатуры для передачи
        kb = pay_course_kb(url_buy=payment.get('pay_url'))

        await state.set_state(PaymentsState.pay_bool)
        await state.update_data(
            pay_token=payment.get('pay_id'),
            pay_sum=plans_price,
            pay_plan=data,
            pay_kb=kb
        )

    match data:
        case 'base':
            await call_back.message.edit_text(text=message_texts.base_course_text,
                                              reply_markup=kb)
        case 'advanced':
            await call_back.message.edit_text(text=message_texts.advanced_course_text,
                                              reply_markup=kb)
        case 'exclusive':
            await call_back.message.edit_text(text=message_texts.exclusive_course_text,
                                              reply_markup=kb)
        case 'all':
            await call_back.message.edit_text(text=message_texts.all_course_text,
                                              reply_markup=kb)
        case 'back':
            await call_back.message.edit_text(text=message_texts.ref_and_course_text,
                                              reply_markup=ref_and_course_kb)
        case _:
            pass

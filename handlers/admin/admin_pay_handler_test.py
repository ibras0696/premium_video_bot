from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import CrudeSubscriptions, CrudePayments, Subscriptions
from keyboards import course_kb, profile_kb, support_kb, ref_and_course_kb, pay_course_kb
from states import PaymentsState
from utils import message_texts
from services import checkout_payment, create_payment

from filters.admin_filter import AdminTypeFilter, AdminCallBackFilter

router = Router()


@router.message(Command('test_pay'), AdminTypeFilter())
async def cmd_test_pay(message: Message, state: FSMContext):
    # Этот хэндлер реагирует на команду /test_pay
    await message.answer(text="Выберите тариф для оплаты:", reply_markup=course_kb)


@router.callback_query(F.data.startswith('course_'), AdminTypeFilter())
async def course_callback_handler(call_back: CallbackQuery, state: FSMContext):
    # Удаление "крутилки"
    await call_back.answer()

    kb = None
    data = call_back.data.replace('course_', '')

    if data in ['all', 'exclusive', 'advanced', 'base']:
        # Цены и описание тарифов (пример)
        plans_price = 1  # Здесь нужно поставить реальные цены
        plans_info = Subscriptions.get_plans().get(data, 'base')

        # Создаем платеж
        payment = create_payment(
            amount=plans_price,
            telegram_id=call_back.message.chat.id,
            description=f'Покупка {plans_info}а',
        )
        # Клавиатура с кнопкой оплаты
        kb = pay_course_kb(url_buy=payment.get('pay_url'))

        await state.set_state(PaymentsState.pay_bool)
        await state.update_data(
            pay_token=payment.get('pay_id'),
            pay_sum=plans_price,
            pay_plan=data,
            pay_kb=kb
        )

    # Редактируем сообщение в зависимости от выбора
    match data:
        case 'base':
            await call_back.message.edit_text(text=message_texts.base_course_text, reply_markup=kb)
        case 'advanced':
            await call_back.message.edit_text(text=message_texts.advanced_course_text, reply_markup=kb)
        case 'exclusive':
            await call_back.message.edit_text(text=message_texts.exclusive_course_text, reply_markup=kb)
        case 'all':
            await call_back.message.edit_text(text=message_texts.all_course_text, reply_markup=kb)
        case 'back':
            await call_back.message.edit_text(text=message_texts.ref_and_course_text, reply_markup=ref_and_course_kb)
        case _:
            pass


@router.callback_query(F.data.startswith('pay_course_'), AdminCallBackFilter())
async def pay_course_callback_handler(call_back: CallbackQuery, state: FSMContext):
    # Удаляем "крутилку"
    await call_back.answer()

    user_id = call_back.message.chat.id

    match call_back.data:
        case 'pay_course_buy':
            data = await state.get_data()
            pay_token = data.get('pay_token')
            pay_plan = data.get('pay_plan')
            pay_kb = data.get('pay_kb')

            sub = CrudeSubscriptions()
            result_course_check = await sub.check_subscription(user_id, pay_plan)

            if result_course_check and getattr(result_course_check, "day_count", 0) > 0:
                await call_back.message.edit_text(
                    text=await message_texts.get_profile_text(user_id),
                    reply_markup=profile_kb
                )
            else:
                result = checkout_payment(pay_token)
                if result:
                    text = await handle_pay(user_id, pay_plan)
                    await call_back.message.edit_text(text=text, reply_markup=profile_kb)
                elif result is None:
                    if call_back.message.text != message_texts.loading_payment_text:
                        await call_back.message.edit_text(text=message_texts.loading_payment_text, reply_markup=pay_kb)
                else:
                    await call_back.message.edit_text(
                        text=message_texts.end_payment_text + '\n\n\n' + await message_texts.get_profile_text(user_id),
                        reply_markup=ref_and_course_kb
                    )
                    await state.clear()

        case 'pay_course_support':
            await call_back.message.edit_text(text=message_texts.support_message_text, reply_markup=support_kb)
            await state.clear()

        case 'pay_course_back':
            await call_back.message.edit_text(text=message_texts.course_text, reply_markup=course_kb)
            await state.clear()

        case _:
            pass


async def handle_pay(user_id: int, plans: str):
    days = Subscriptions.get_days_plans().get(plans, 1)
    price = Subscriptions.get_price_plans().get(plans, 1)

    sub = CrudeSubscriptions()
    await sub.add_subscription(user_id, plans, days, price)

    paym = CrudePayments()
    await paym.add_payment(user_id, plans, days, price)

    return message_texts.accept_course_text + '\n\n' + await message_texts.get_profile_text(user_id)

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import CrudeSubscriptions, CrudePayments, Subscriptions
from keyboards import course_kb, profile_kb, support_kb, ref_and_course_kb
from utils import message_texts
from services import checkout_payment

router = Router()


@router.callback_query(F.data.startswith('pay_course_'))
async def pay_course_cmd(call_back: CallbackQuery, state: FSMContext):
    user_id = call_back.message.chat.id
    match call_back.data:
        case 'pay_course_buy':
            data = await state.get_data()
            # Токен платежа
            pay_token = data.get('pay_token')
            # Тариф
            pay_plan = data.get('pay_plan')
            # Сохранение Клавиатуры
            pay_kb = data.get('pay_kb')

            # Добавление подписки
            sub = CrudeSubscriptions()
            result_course_check = await sub.check_subscription(user_id, pay_plan)
            if result_course_check and getattr(result_course_check, "day_count", 0) > 0:
                await call_back.message.edit_text(
                    text=await message_texts.get_profile_text(user_id),
                    reply_markup=profile_kb
                )
            else:
                # Получение данных при оплате
                result = checkout_payment(pay_token)
                # В случае успешной оплаты
                if result:
                    text = await handle_pay(user_id, pay_plan)
                    await call_back.message.edit_text(text=text, reply_markup=profile_kb)
                # В случае если время в ожидании
                elif result is None:
                    if call_back.message.text != message_texts.loading_payment_text:
                        await call_back.message.edit_text(text=message_texts.loading_payment_text, reply_markup=pay_kb)
                # В случае если истекло время платежа
                else:
                    await call_back.message.edit_text(
                        text=message_texts.end_payment_text + '\n\n\n' + await message_texts.get_profile_text(call_back.message.chat.id),
                        reply_markup=ref_and_course_kb
                    )
                    await state.clear()

        case 'pay_course_support':
            await call_back.message.edit_text(text=message_texts.support_message_text, reply_markup=support_kb)

        case 'pay_course_back':
            await call_back.message.edit_text(message_texts.course_text, reply_markup=course_kb)
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

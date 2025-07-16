from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import CrudeSubscriptions, CrudePayments, Subscriptions
from keyboards import course_kb, profile_kb, support_kb
from utils import message_texts

router = Router()


@router.callback_query(F.data.startswith('pay_course_'))
async def pay_course_cmd(call_back: CallbackQuery, state: FSMContext):
    user_id = call_back.message.chat.id
    match call_back.data:
        case 'pay_course_pay':
            data = await state.get_data()
            plans = data.get('course', 'base')
            # Добавление подписки
            sub = CrudeSubscriptions()
            result_course_check = await sub.check_subscription(user_id, plans)
            if result_course_check and result_course_check.day_count > 0:
                await call_back.message.edit_text(text=await message_texts.get_profile_text(user_id),
                                                  reply_markup=profile_kb)
            else:
                days = Subscriptions.get_days_plans().get(plans, 1)
                price = Subscriptions.get_price_plans().get(plans, 1)
                await sub.add_subscription(
                    telegram_id=user_id,
                    plan=plans,
                    day_count=days,
                    price=price
                )
                # дОбавление платежа в бд
                paym = CrudePayments()
                await paym.add_payment(
                    telegram_id=user_id,
                    plan=plans,
                    day_count=days,
                    pay_sum=price
                )

                await call_back.message.edit_text(text=message_texts.accept_course_text + await message_texts.get_profile_text(user_id),
                                                  reply_markup=profile_kb)

        case 'pay_course_support':
            await call_back.message.edit_text(text=message_texts.support_message_text, reply_markup=support_kb)
        case 'pay_course_back':
            await call_back.message.edit_text(message_texts.course_text, reply_markup=course_kb)
        case _:
            pass
    await state.clear()
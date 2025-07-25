from aiogram import Router, F, Bot
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database import CrudeUser
from keyboards import take_of_confirm_kb, ref_and_course_kb, refer_kb
from states import TakeOffManyState
from utils import message_texts
from config import ADMIN_IDS

# Инициализация роутера
router = Router()


# Обработка сообщения от пользователя, когда он находится в состоянии ввода данных для снятия средств
@router.message(TakeOffManyState.telegram_id)
async def take_start_cmd(message: Message, state: FSMContext):
    text = message.text.split(' ')  # Разделяем сообщение на части (ожидается: сумма, номер, банк)

    try:
        if text and len(text) == 3:
            # Парсим сумму, номер счёта (или телефона), банк
            take_sum = int(text[0].strip())
            take_number = int(text[1].strip())
            take_bank = text[2].strip()

            # Проверка на минимальную сумму
            if take_sum >= 500:
                # Создание текста чека для подтверждения
                msg_text = message_texts.take_of_many_loading_text(message.chat.id, take_sum, take_number, take_bank)

                # Отправка пользователю подтверждения с кнопками
                await message.answer(
                    text=msg_text,
                    reply_markup=take_of_confirm_kb
                )

                # Сохраняем данные во временное хранилище FSM
                await state.update_data(
                    telegram_id=message.chat.id,
                    take_sum=take_sum,
                    take_bank=take_bank,
                    take_number=take_number,
                    take_text=msg_text
                )
            else:
                # Если сумма меньше 500 — предупреждаем пользователя
                await message.answer(text=message_texts.warning_take_off_text, reply_markup=ref_and_course_kb)
                await state.clear()  # Сбрасываем состояние
        else:
            # Если данные введены не в том формате — подсказываем правильный
            await message.answer(text=message_texts.take_of_text, reply_markup=refer_kb())

    except ValueError:
        # Если не удалось преобразовать сумму или номер — подсказываем правильный формат
        await message.answer(text=message_texts.take_of_text, reply_markup=refer_kb())


# Обработка нажатия на кнопки подтверждения / отмены снятия
@router.callback_query(F.data.startswith('take_confirm_'))
async def take_confirm_cmd(call_back: CallbackQuery, state: FSMContext, bot: Bot):
    call = call_back.data.replace('take_confirm_', '')  # Получаем тип действия: 'con' или 'back'
    user_id = call_back.message.chat.id
    # Удаление мигающих кнопок
    await call_back.answer()

    match call:
        case 'con':
            # Если пользователь подтвердил снятие — редактируем сообщение, уведомляем и обрабатываем
            await call_back.message.edit_text(
                message_texts.take_push_message_text,
                reply_markup=ref_and_course_kb
            )

            # Получаем данные из FSM
            data = await state.get_data()
            telegram_id = data.get('telegram_id')
            take_sum = data.get('take_sum')
            take_text = data.get('take_text')

            # Уменьшаем баланс пользователя на указанную сумму
            await CrudeUser().update_user(telegram_id=telegram_id, reduce_balance=take_sum)

            for admin in ADMIN_IDS:
                # Отправляем уведомление администратору о снятии средств
                await bot.send_message(
                    admin,
                    message_texts.admin_take_confirm_text(take_text)
                )

        case 'back':
            # Если пользователь нажал "назад" — возвращаемся в главное меню
            await call_back.message.edit_text(
                await message_texts.refer_id_text(telegram_id=user_id),
                reply_markup=refer_kb(take=True)
            )

        case _:
            # Непредусмотренное значение — игнорируем
            pass

    await state.clear()  # Очищаем состояние в любом случае

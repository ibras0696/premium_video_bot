import traceback
import logging
from typing import Callable, Dict, Any, Awaitable

from datetime import datetime

from aiogram.types import Update
from aiogram import BaseMiddleware, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ChatMemberUpdated, CallbackQuery

from config import ADMIN_IDS, grps
from database import CrudeSubscriptions, Subscriptions


class SubscriptionMiddleware(BaseMiddleware):
    def __init__(self):
        self.group_tariffs = Subscriptions.get_group_ids()

    async def __call__(
            self,
            handler: Callable,
            event: Any,  # Принимаем любой тип события
            data: Dict[str, Any]
    ) -> Any:
        bot: Bot = data['bot']
        chat_id = None
        user_id = None

        # Обработка разных типов событий
        if isinstance(event, Message):
            # Для обычных сообщений
            chat_id = str(event.chat.id)
            user_id = event.from_user.id

        elif isinstance(event, ChatMemberUpdated):
            # Для событий входа/выхода участников
            if event.old_chat_member.status == "left" and event.new_chat_member.status == "member":
                chat_id = str(event.chat.id)
                user_id = event.new_chat_member.user.id
            else:
                # Пропускаем события, не связанные с вступлением
                return await handler(event, data)

        elif isinstance(event, CallbackQuery) and event.message:
            # Для callback-запросов из групп
            chat_id = str(event.message.chat.id)
            user_id = event.from_user.id

        else:
            # Пропускаем неизвестные типы событий
            return await handler(event, data)

        # Определяем тариф по ID чата
        plan = None
        for tariff, grp_id in self.group_tariffs.items():
            if str(grp_id) == chat_id:
                plan = tariff
                break

        if not plan:
            return await handler(event, data)

        try:
            # Проверяем подписку
            subscription = await CrudeSubscriptions().check_subscription(user_id, plan)

            if not subscription or subscription.day_count <= 0:
                try:
                    # Кикаем пользователя
                    await bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
                    await bot.unban_chat_member(chat_id=chat_id, user_id=user_id)
                    logging.info(f"❌ {user_id} кикнут из {chat_id}, нет подписки на {plan}")

                    # Отправляем уведомление админу
                    for admin_id in ADMIN_IDS:
                        await bot.send_message(
                            admin_id,
                            f"👤 Пользователь {user_id} исключён из группы {chat_id}\n"
                            f"📋 Причина: отсутствует активная подписка на тариф {plan}"
                        )

                except TelegramBadRequest as e:
                    logging.error(f"⚠️ Ошибка кика в {chat_id}: {e}")

        except Exception as e:
            logging.exception(f"❌ Ошибка проверки подписки: {e}")

        return await handler(event, data)

class ErrorMiddleware(BaseMiddleware):
    """
    Middleware для глобального перехвата ошибок в Aiogram 3.
    При возникновении исключений:
    - логирует ошибку в консоль;
    - отправляет уведомление админу;
    - записывает информацию в базу данных.
    """

    async def __call__(
        self,
        handler: Callable[[Update, dict], Awaitable[Any]],
        event: Update,
        data: dict
    ) -> Any:
        try:
            return await handler(event, data)

        except Exception as e:
            bot: Bot = data.get("bot")
            tb = traceback.format_exc()
            logging.error(f"Ошибка при обработке события: {tb}")

            # Безопасно определяем Telegram ID
            telegram_id = None
            telegram_name = None
            if event.message:
                telegram_id = event.message.from_user.id
                telegram_name = event.message.from_user.username
            elif event.callback_query:
                telegram_id = event.callback_query.from_user.id
                telegram_name = event.callback_query.from_user.username
            elif event.inline_query:
                telegram_id = event.inline_query.from_user.id
                telegram_name = event.inline_query.from_user.username

            # Получаем текущую дату и время
            now = datetime.now()

            # Форматируем в нужный формат
            formatted_time = now.strftime("%H:%M %d.%m.%Y")

            # Отправка админу
            if bot:
                try:
                    # for tg_id in ADMIN_IDS:
                    await bot.send_message(
                        chat_id=ADMIN_IDS[1],
                        text=f"❌ Ошибка!"
                             f"\nТелеграм ID: {telegram_id}"
                             f"\nТелеграм Ник: {telegram_name}"
                             f"\nВремя: {formatted_time}"
                             f"\n\n<b>{type(e).__name__}:</b> {e}\n\n<pre>{tb[-700:-1]}</pre>",
                        parse_mode="HTML"
                    )
                except Exception as ex:
                    print(f'Ошибк: {ex}')

'''

Объясняю ситуацию я сделал логер для отдельных 4 тарифов то есть 4х групп
он обрабатывает логи и проверяет есть ли подписка тех кто вошел или вышел
и кикает тех у кого она закончилась или нет
проблемы как ты сказал начались с евентами
я отвечу на твои вопросы или сделаю то шо ты скажешь
вот логер который там есть

import logging
import traceback
from datetime import datetime
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from aiogram.types import Update

from config import ADMIN_IDS, grps
from database import CrudeSubscriptions, Subscriptions


class SubscriptionMiddleware(BaseMiddleware):
    def __init__(self):
        self.group_tariffs = Subscriptions.get_group_ids()

    async def __call__(
        self,
        handler: Callable,
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        message: Message = event

        chat_id = str(message.chat.id)
        telegram_id = message.from_user.id

        # Определяем тариф по chat_id
        plan = None
        for tariff, grp_id in self.group_tariffs.items():
            if str(grp_id) == chat_id:
                plan = tariff
                break

        if not plan:
            return await handler(event, data)

        try:
            subscription = await CrudeSubscriptions().check_subscription(telegram_id, plan)

            if not subscription or subscription.day_count <= 0:
                try:
                    await message.bot.ban_chat_member(chat_id=chat_id, user_id=telegram_id)
                    await message.bot.unban_chat_member(chat_id=chat_id, user_id=telegram_id)
                    print(f"❌ {telegram_id} кикнут из {chat_id}, нет активной подписки на {plan}")
                except TelegramBadRequest as e:
                    print(f"⚠️ Ошибка при кике: {e}")
        except Exception as e:
            print(f"❌ Ошибка при проверке подписки: {e}")

        return await handler(event, data)
'''
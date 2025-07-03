import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.exceptions import TelegramBadRequest

from config import TOKEN_BOT

from middlewares import ErrorMiddleware

from database import init_db

from handlers import router


bot_tg = Bot(token=TOKEN_BOT)
dp = Dispatcher()


async def main():
    # Инициализация БД
    await init_db()
    # Подключение Мидлов
    dp.update.middleware(ErrorMiddleware())
    # Подключение роутера
    dp.include_router(router)
    # Удаление прежних вебхуков
    await bot_tg.delete_webhook(drop_pending_updates=True)

    # Запуск
    await dp.start_polling(bot_tg)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except TelegramBadRequest as e:
        logging.error(f"Telegram API error: {e}")
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.critical(f"Критическая ошибка: {e}", exc_info=True)

# Ссылка на план нейронки https://chatgpt.com/c/68642b54-32f4-8005-8be1-f4b5d55ebc0f


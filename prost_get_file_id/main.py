import logging
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
import re

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

# 🔐 Токен бота (в проде храни в .env)
TOKEN = '8174103204:AAFKSmgjdpng3sCEVd4z6PubGy9Mfn-el8s'
if not TOKEN:
    logging.error("Токен бота не указан!")
    exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()


def escape_markdown(text: str) -> str:
    # Символы, которые надо экранировать в MarkdownV2
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    # Экранируем каждый спецсимвол, используя re.sub и обратный слэш
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


# 💬 Обработка /start и /help
@dp.message(Command(commands=["start", "help"]))
async def send_welcome(message: Message):
    logging.info(f"Команда от {message.from_user.id}")
    await message.answer("Бот работает. Отправьте сообщение или видео.")


# 💬 Эхо для обычных сообщений
@dp.message()
async def echo(message: Message):
    logging.info(f"Сообщение от {message.from_user.id}: {message.text}")
    await message.answer("Сообщение получено!")


# 📢 Обработка постов из канала
@dp.channel_post()
async def handle_channel_post(message: Message):
    logging.info(f"Пост из канала {message.chat.id}")

    if message.video:
        video_id = message.video.file_id
        logging.info(f"Видео file_id: {video_id}")
        # escaped_id = escape_markdown(video_id)
        # await message.reply(
        #     f"🎥 Получен video file_id:\n`{escaped_id}`",
        #     parse_mode=ParseMode.MARKDOWN_V2
        # )

    elif message.photo:
        photo_id = message.photo[-1].file_id
        logging.info(f"Фото file_id: {photo_id}")
        # escaped_id = escape_markdown(photo_id)
        # await message.reply(
        #     f"🖼 Получен photo file_id:\n`{escaped_id}`",
        #     parse_mode=ParseMode.MARKDOWN_V2
        # )

    elif message.document:
        doc_id = message.document.file_id
        logging.info(f"Документ file_id: {doc_id}")
        # escaped_id = escape_markdown(doc_id)
        # await message.reply(
        #     f"📄 Получен document file_id:\n`{escaped_id}`",
        #     parse_mode=ParseMode.MARKDOWN_V2
        # )

    else:
        await message.reply("Пост получен, но не содержит видео, фото или документ.")


# 🚀 Запуск бота
async def main():
    logging.info("Запуск бота...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(main())
    except Exception as e:
        logging.exception(f"Ошибка при запуске бота: {e}")

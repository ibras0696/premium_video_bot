from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from utils import admin_message_text
from keyboards import admin_kb
from filters.admin_filter import  AdminTypeFilter, AdminCallBackFilter

router = Router()

# Обработчик
@router.message(Command('admin'), AdminTypeFilter())
async def admin_start_cmd(message: Message):
    """
    Обработка команды /admin, отправляет приветственное сообщение администратору.
    """
    await message.answer(
        text=admin_message_text.start_test,
        reply_markup=admin_kb.cmd_admin_kb  # Здесь можно добавить клавиатуру для администратора
    )


@router.callback_query(F.data.startswith('admin_'), AdminCallBackFilter())
async def update_admin_start_kb(call_back: CallbackQuery):
    action = call_back.data.replace('admin_', '')

    match action:
        case 'subs':
            text = await admin_message_text.subscription_text()
        case 'users':
            text = await admin_message_text.users_text()
        case 'payments':
            text = await admin_message_text.payments_text()
        case _:
            text = "Неизвестная команда."
    try:
        await call_back.message.edit_text(
            text=text,
            reply_markup=admin_kb.cmd_admin_kb  # оставляем кнопки, чтобы можно было снова нажимать
        )
    # Пропуск при повторном нажатии
    except TelegramBadRequest:
        pass

    await call_back.answer()  # закрыть "часики"


# Доп Роутер для получения айди файла
@router.message(F.video, AdminTypeFilter())
async def get_file_id(message: Message):
    """
    Обработчик для получения ID видеофайла.
    """
    video = message.video
    if video:
        file_id = video.file_id
        await message.answer(f"File ID: {file_id}")
    else:
        await message.answer("Видео не найдено.")

    # await message.delete()
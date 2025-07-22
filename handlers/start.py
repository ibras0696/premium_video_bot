from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.exceptions import TelegramBadRequest

from keyboards import start_kb, ref_and_course_kb, course_kb, profile_kb, refer_kb
from utils import message_texts
from static.start_video_path import get_start_mov_file, start_mov_file_id, save_new_start_video_id
from database import CrudeUser

router = Router()


# Обработка старта через реферальную ссылку
@router.message(CommandStart(deep_link=True))
async def start_cmd(message: Message, state: FSMContext, command: CommandStart):
    await state.clear()
    ref_id = command.args

    try:
        if ref_id:
            r_d = int(ref_id)
            await CrudeUser().add_user(telegram_id=message.from_user.id,
                                       user_name=message.from_user.username,
                                       referral_id=r_d)
            await send_start_video(message)
    except ValueError:
        pass
    except Exception as ex:
        raise Exception(f'Ошибка при обработке реферальной ссылки: {ex}')


# Обработка обычного старта
@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await CrudeUser().add_user(telegram_id=message.from_user.id,
                               user_name=message.from_user.username)

    await send_start_video(message)


@router.callback_query(F.data == 'start')
async def start_query(call_back: CallbackQuery):
    await call_back.message.delete()
    # Отправляем сообщение с реферальной ссылкой
    await call_back.message.answer(message_texts.ref_and_course_text, reply_markup=ref_and_course_kb)


# Обработка кнопки реф ссылки
@router.callback_query(F.data.startswith('get_start_'))
async def get_start_cmd(call_back: CallbackQuery):
    user_id = call_back.message.chat.id
    match call_back.data:
        case 'get_start_course':
            await call_back.message.edit_text(message_texts.course_text, reply_markup=course_kb)
        case 'get_start_profile':
            await call_back.message.edit_text(text=await message_texts.get_profile_text(user_id),
                                              reply_markup=profile_kb)
        case 'get_start_ref':
            await call_back.message.edit_text(await message_texts.refer_id_text(telegram_id=user_id),
                                              reply_markup=refer_kb(take=True))
        case _:
            pass


# Отправка файла по айди или локально
async def send_start_video(message: Message):
    global start_mov_file_id
    try:
        if start_mov_file_id:
            await message.answer_video(
                caption=message_texts.start_text,
                video=start_mov_file_id,
                reply_markup=start_kb
            )
        else:
            # Нет file_id — отправляем локальный файл сразу
            video_file = get_start_mov_file()
            sent_message = await message.answer_video(
                caption=message_texts.start_text,
                video=video_file,
                reply_markup=start_kb
            )
            new_file_id = sent_message.video.file_id
            save_new_start_video_id(new_file_id)
    except TelegramBadRequest as e:
        # Ошибка из-за неверного file_id — отправляем локальный файл и обновляем id
        if "file_id" in str(e).lower() or "wrong file identifier" in str(e).lower():
            video_file = get_start_mov_file()
            sent_message = await message.answer_video(
                caption=message_texts.start_text,
                video=video_file,
                reply_markup=start_kb
            )
            new_file_id = sent_message.video.file_id
            save_new_start_video_id(new_file_id)
        else:
            # Проброс других ошибок
            raise
# # Тестовое получение файл айди видео
# @router.message(F.video)
# async def get_file_id(message: Message):
#     if message.video:
#         video_id = message.video.file_id
#         await message.answer(f"🎥 Получен video file_id:\n{video_id}")
#     else:
#         await message.answer("Пожалуйста, отправьте видео для получения file_id.")
#
# @router.message(F.text)
# async def send_video_file_id(message: Message):
#     if message.text:
#         await message.answer_video(video=message.text, caption="Вот ваше видео!")
#     else:
#         await message.answer("Отправьте 'send video' для получения видеофайла.")

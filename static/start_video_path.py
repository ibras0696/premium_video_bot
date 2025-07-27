import os
from aiogram.types import FSInputFile

start_mov_file_id = 'BAACAgIAAxkBAAMGaIalqQSRrQ7goRq2m2MhrKP_wrAAAryCAALNswlITsE8xx4dOhM2BA'

# Функция для получения пути к видеофайлу, который будет отправлен пользователю при нажатии кнопки "Старт".
def get_start_mov_file() -> FSInputFile:
    """
    Функция для получения пути к видеофайлу, который будет отправлен пользователю при нажатии кнопки "Старт".
    :return: FSInputFile с объектом файла, который содержит путь к видео.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(base_dir, 'old_start_mov.mov')
    file_path = os.path.join(base_dir, 'old_start_video.mp4')
    return FSInputFile(file_path)

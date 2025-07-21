import os
from aiogram.types import FSInputFile

# Функция для получения пути к видеофайлу, который будет отправлен пользователю при нажатии кнопки "Старт".
def get_start_mov_file() -> FSInputFile:
    """
    Функция для получения пути к видеофайлу, который будет отправлен пользователю при нажатии кнопки "Старт".
    :return: FSInputFile с объектом файла, который содержит путь к видео.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'start_mov.mov')
    return FSInputFile(file_path)

import os
from aiogram.types import FSInputFile

#rt_mov_file_id = 'BAACAgIAAyEFAASai0lTAAMWaH9pNdICvCF-9QViHUxW93tZkTkAAkJxAAJ6rPhLIk_6M1BcfGA2BA'
# start_mov_file_id = 'BAACAgIAAyEFAASai0lTAAMcaH_I_dC_hshKUy33HKr2YRDz9BIAAkJxAAJ6rPhLp_bkIAVQ7TI2BA'
start_mov_file_id = 'BAACAgIAAyEFAASai0lTAAMcaH_I_dC_hshKUy33HKr2YRDz9BIAAkJxAAJ6rPhLp_bkIAVQ7TI2BA'


# Функция для получения пути к видеофайлу, который будет отправлен пользователю при нажатии кнопки "Старт".
def get_start_mov_file() -> FSInputFile:
    """
    Функция для получения пути к видеофайлу, который будет отправлен пользователю при нажатии кнопки "Старт".
    :return: FSInputFile с объектом файла, который содержит путь к видео.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'old_start_mov.mov')
    return FSInputFile(file_path)

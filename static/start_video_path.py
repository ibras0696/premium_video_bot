import os
from aiogram.types import FSInputFile

mov_file_id = 'BAACAgIAAyEFAASai0lTAAMcaH_I_dC_hshKUy33HKr2YRDz9BIAAkJxAAJ6rPhLp_bkIAVQ7TI2BA'

# Путь к текстовому файлу, где хранится актуальный file_id
FILE_ID_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "start_video_id.txt")

# Путь к локальному видеофайлу
VIDEO_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "new_start_video.mp4")


def get_start_mov_file() -> FSInputFile:
    """
    Возвращает FSInputFile с путем к видеофайлу.
    """
    return FSInputFile(VIDEO_FILE_PATH)


def save_new_start_video_id(new_id: str):
    """
    Сохраняет новый file_id в переменную и файл.
    """
    global start_mov_file_id
    start_mov_file_id = new_id
    with open(FILE_ID_PATH, "w") as f:
        f.write(new_id.strip())


def load_start_video_id() -> str | None:
    """
    Загружает file_id из файла, если он существует.
    """
    if os.path.exists(FILE_ID_PATH):
        with open(FILE_ID_PATH, "r") as f:
            return f.read().strip()
    return None


# Загружаем file_id при импорте
start_mov_file_id = load_start_video_id()

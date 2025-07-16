# Базовый образ Python 3.12
FROM python:3.12-slim-bookworm

# Установка рабочей директории
WORKDIR /app

# Копирование файла зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . .

## Запуск асинхронных тестов
#RUN pytest -v --asyncio-mode=strict

# Запуск приложения (если тесты прошли)
CMD ["python", "main.py"]
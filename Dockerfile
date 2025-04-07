# Базовый образ Python
FROM python:3.12-slim

# Установка зависимостей для mysqlclient
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

# Установка Python-зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . .

# Переменные окружения
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Порт для Flask
EXPOSE 5000

# Команда запуска
CMD ["flask", "run"]
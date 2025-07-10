FROM python:3.11-slim

WORKDIR /app

# Копируем только requirements.txt сначала — для кэширования слоя установки зависимостей
COPY requirements/ ./requirements/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements/requirements-all.txt

# Копируем весь остальной код
COPY . .

# Создаем пользователя "app" и меняем владельца папки /app
RUN adduser --disabled-password app && chown -R app /app

# Переключаемся на пользователя app (без прав root)
USER app

# Добавляем HEALTHCHECK для проверки работоспособности сервиса
HEALTHCHECK CMD curl -f http://localhost:8000/health || exit 1

# Запускаем uvicorn на 0.0.0.0:8000, чтобы контейнер был доступен извне
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

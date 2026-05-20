# --- Этап 1: Сборка (Builder) ---
# Используем образ с компиляторами для сборки зависимостей.
FROM python:3.14-slim-bookworm AS builder

# Устанавливаем рабочую директорию
WORKDIR /app

# 1. Установить системные зависимости для компиляции (ruff, sqlalchemy и др.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Установить uv (менеджер пакетов)
RUN pip install --no-cache-dir --upgrade uv

# Копируем файлы проекта и устанавливаем зависимости
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock

# Устанавливаем зависимости из lock-файла.
# --frozen гарантирует использование только разрешенных версий.
RUN uv sync --frozen --no-cache-dir

# Копируем исходный код приложения
COPY . .


# --- Этап 2: Финальный (Runtime) ---
# Используем чистый runtime-образ без компиляторов для безопасности и размера.
FROM python:3.14-slim-bookworm

WORKDIR /app

# Копируем установленные библиотеки из этапа сборки
COPY --from=builder /usr/local /usr/local

# Копируем исходный код и наш entrypoint-скрипт
COPY --from=builder /app /app

# Настройка переменных окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=UTC \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

EXPOSE ${UVICORN_PORT} 

COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/bin/sh", "/app/docker-entrypoint.sh"]
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "${UVICORN_PORT}"]

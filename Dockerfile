# --- Этап 1: Сборка (Builder) ---
FROM python:3.14-slim-bookworm AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade uv

COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
RUN uv sync --frozen --no-cache-dir
COPY . .

# --- Этап 2: Финальный (Runtime) ---
FROM python:3.14-slim-bookworm

WORKDIR /app
RUN pip install --no-cache-dir --upgrade uv
COPY --from=builder /app/pyproject.toml /app/
COPY --from=builder /app/uv.lock /app/
RUN uv pip install --system --no-cache-dir .
COPY --from=builder /app /app
COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=UTC \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

RUN groupadd -r appuser && useradd -r -s /bin/false -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

ENTRYPOINT ["/bin/sh", "/app/docker-entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]

#!/bin/sh

wait_for_db() {
  echo "Waiting for PostgreSQL to be ready..."
  until pg_isready -U "$POSTGRES_USER" -h db -p 5432 --timeout=0; do
    >&2 echo "PostgreSQL is unavailable - sleeping"
    sleep 1
  done
  echo "PostgreSQL is up!"
}

run_migrations() {
  echo "Running Alembic migrations..."
  # Эта команда выполнит миграции, используя настройки из .env
  alembic upgrade head || { echo "Alembic migrations failed!"; exit 1; }
  echo "Migrations completed successfully."
}

# --- Main ---
wait_for_db
run_migrations

# Запускаем основную команду (uvicorn)
exec "$@"

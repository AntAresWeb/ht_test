#!/bin/sh
set -e

run_migrations() {
  echo "Running Alembic migrations..."
  alembic upgrade head 
  echo "Migrations completed successfully."
}

run_migrations

echo "Starting the application..."
exec "$@" --port=${UVICORN_PORT:-8000}
#!/bin/sh

# Wait until Postgres is ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 2
done
echo "Database is ready, starting server..."

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:5000 app:app


#!/bin/sh

# Extract host and port dynamically using Python from DATABASE_URL, defaulting to db:5432
DB_HOST=$(python3 -c "import os, urllib.parse; u=urllib.parse.urlsplit(os.getenv('DATABASE_URL', '')); print(u.hostname or 'db')")
DB_PORT=$(python3 -c "import os, urllib.parse; u=urllib.parse.urlsplit(os.getenv('DATABASE_URL', '')); print(u.port or 5432)")

echo "Waiting for database at $DB_HOST:$DB_PORT..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 2
done
echo "Database is ready, starting server..."

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:5000 app:app


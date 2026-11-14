#!/bin/sh
set -e

echo "==> Running database migrations..."
python manage.py migrate --noinput

PORT_NUM="${PORT:-8000}"
echo "==> Starting Gunicorn on port ${PORT_NUM}..."
exec gunicorn config.wsgi:application --bind "0.0.0.0:${PORT_NUM}" --workers 2 --threads 2

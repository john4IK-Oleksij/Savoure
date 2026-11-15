FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Collect static files via WhiteNoise
RUN python manage.py collectstatic --noinput

# Pre-populate media dishes so uploaded images are baked in and never lost
RUN mkdir -p media/dishes media/dishes/2026/11 && \
    cp static/dish-list/* media/dishes/ && \
    cp static/dish-list/* media/dishes/2026/11/

EXPOSE 8000

# sh -c ensures the dynamic $PORT provided by Railway is properly expanded by the shell
CMD sh -c "python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:\${PORT:-8000}"

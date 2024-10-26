FROM python:3.11-slim


RUN apt-get update && apt-get install -y curl && apt-get clean
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app/
COPY .env /app/.env.docker



CMD python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='root@example.com').exists() or User.objects.create_superuser('root@example.com', 'root')" \
    && python manage.py collectstatic --no-input \
    && python manage.py initialize_db \
    && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --log-level info


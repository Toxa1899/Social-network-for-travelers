FROM python:3.11-slim

WORKDIR /app

COPY . /app/
COPY .env /app/.env.docker

RUN pip install poetry
RUN poetry install --no-dev --only docker


RUN python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='root@example.com').exists() or User.objects.create_superuser( 'root@example.com', 'root')" \
    && python manage.py collectstatic --no-input \


CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--log-level", "info"]



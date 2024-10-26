db:
	python3 manage.py makemigrations
	python3 manage.py migrate

static:
	python3 manage.py collectstatic

run:
	python3 manage.py runserver
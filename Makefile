install:
	poetry install

init:
	poetry init

dev_server:
	poetry run python manage.py runserver

unic_server:
	export DJANGO_SETTINGS_MODULE=fourth.settings
	gunicorn fourth.wsgi

requiremets.txt:
	poetry export -f requirements.txt --output requirements.txt

push_heroku:
	@git push heroku main

run_heroku:
	heroku ps:scale web=1

lint:
	poetry run flake8 fourth

makemigrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

shell:
	@poetry run python manage.py shell

test:
	poetry run python -Wa manage.py test

bash_heroku:
	@heroku run bash

install:
	poetry install

init:
	poetry init

dev_server:
	poetry run python manage.py runserver

unic_server:
	export DJANGO_SETTINGS_MODULE=task_manager.settings
	gunicorn task_manager.wsgi

requiremets.txt:
	poetry export -f requirements.txt --output requirements.txt

push_heroku:
	git push heroku main

run_heroku:
	heroku ps:scale web=1

lint:
	poetry run flake8 task_app,

makemigrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

shell:
	poetry run python manage.py shell

test:
	poetry run python manage.py test task_app/tests/

bash_heroku:
	heroku run bash

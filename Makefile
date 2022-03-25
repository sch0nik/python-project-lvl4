install:
	poetry install

init:
	poetry init

dev_server:
	poetry run python manage.py runserver

gunic_server:
	export DJANGO_SETTINGS_MODULE=task_manager.settings
	gunicorn task_manager.wsgi

requiremets.txt:
	poetry export -f requirements.txt --output requirements.txt

push_heroku:
	git push heroku main

lint:
	poetry run flake8

makemigrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

shell:
	poetry run python manage.py shell

test:
	poetry run python manage.py test tests/

tagged_tests:
	poetry run python manage.py test --tag=current tests/

bash_heroku:
	heroku run bash

collectstatic:
	poetry run python manage.py collectstatic

coverage:
	poetry run coverage run manage.py test
	poetry run coverage xml
	poetry run coverage report

dumpdata:
	poetry run python manage.py dumpdata --indent 4 --exclude=auth --exclude=contenttypes --output fixtures.json

.PHONY: init, install, collectstatic, bash_heroku, test, shell, migrate, makemigrations, lint, push_heroku, requiremets.txt, gunic_server, dev_server
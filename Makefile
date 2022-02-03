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
	git push heroku main

run_heroku:
	heroku ps:scale web=1
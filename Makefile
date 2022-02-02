init:
	poetry init

dev_server:
	poetry run python manage.py runserver

unic_server:
	export DJANGO_SETTINGS_MODULE=fourth.settings
	gunicorn fourth.wsgi

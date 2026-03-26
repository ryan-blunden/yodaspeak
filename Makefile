.PHONY: install dev-server

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements/local.txt
	.venv/bin/python manage.py migrate

dev-server:
	.venv/bin/python manage.py runserver 0.0.0.0:8000

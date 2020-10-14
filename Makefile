SHELL := /bin/bash

help:
	@echo "Usage:"
	@echo " make help      -- display this help"
	@echo " make install   -- install requirements and set up the database"
	@echo " make test      -- run tests"

install:
	pip install -r requirements.txt
	if [ `psql -t -c "SELECT COUNT(1) FROM pg_catalog.pg_database WHERE datname = 'coding_test'"` -eq 0 ]; then \
		psql  -c "CREATE DATABASE coding_test"; \
	fi
	python manage.py migrate

test:
	@python manage.py test --keepdb

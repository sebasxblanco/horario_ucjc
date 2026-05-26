#!/bin/bash
set -e
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_datos
python manage.py seed_admin
python manage.py seed_profesores
exec gunicorn config.wsgi --bind 0.0.0.0:$PORT --workers 2 --log-file -

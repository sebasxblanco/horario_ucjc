web: gunicorn config.wsgi --log-file - --workers 2
release: python manage.py migrate --noinput && python manage.py seed_datos && python manage.py seed_profesores

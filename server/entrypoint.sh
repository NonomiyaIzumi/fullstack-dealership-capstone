#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py populate
python manage.py bootstrap_admin

exec gunicorn djangoproj.wsgi:application --bind "0.0.0.0:${PORT:-8000}"

#!/bin/sh
set -e

#migrate
python /code/manage.py migrate --noinput

exec "$@"

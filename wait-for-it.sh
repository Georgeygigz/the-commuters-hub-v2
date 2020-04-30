#!/bin/bash
set -e


until psql $DATABASE_URL -c '\l'; do
    >&2 echo "Postgres is unavailable - sleeping"
    echo ' '
    echo ' '
    echo "<<<<<<<<<<<<<<<<<<<<<<<<<Waiting Postgres to start>>>>>>>>>>>>>>>>>>>>>"
    sleep 10
    echo ' '
    echo ' '
done

>&2  echo "<<<<<<<<<<<<<<<<<<<<<<<<<Postgres is up and running>>>>>>>>>>>>>>>>>>>>>"
    echo ' '
    echo ' '

if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
    python manage.py migrate --noinput
fi

exec "$@"

#!/bin/bash

# source /root/.local/share/virtualenvs/app-*/bin/activate
export $(grep -v '^#' .env | xargs)


echo $CURRENT_UID
# pipenv shell
echo "<<<<<<<<<< Export LANG to the Env>>>>>>>>>>"
echo ' '
echo ' '

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

echo "<<<<<<<< Database Setup and Migrations Starts >>>>>>>>>"
echo ' '
echo ' '
sleep 10
# Run database migrations
python manage.py migrate

echo ' '
echo ' '
sleep 5
echo "<<<<<<< Database Setup and Migrations Complete >>>>>>>>>>"
echo " "
echo ' '
echo "<<<<<<< Collecting static files >>>>>>>>>>"
echo ' '
yes | python manage.py collectstatic --noinput

echo " "
echo ' '
echo "<<<<<<<<<<<<<<<<<<<< START Celery >>>>>>>>>>>>>>>>>>>>>>>>"
echo ' '

# start Celery worker
celery -A app worker -l info --pool=gevent --concurrency=500 &

# start celery beat
# celery -A celery_conf.celery_periodic_scheduler beat --loglevel=info &
echo ' '
echo ' '
sleep 5
echo "<<<<<<<<<<<<<<<<<<<< START API >>>>>>>>>>>>>>>>>>>>>>>>"
echo ' '
echo ' '

# python manage.py runserver 0.0.0.0:8000
# Start the API with gunicorn
gunicorn --bind 0.0.0.0:8000 app.wsgi --reload --access-logfile '-' --workers 2

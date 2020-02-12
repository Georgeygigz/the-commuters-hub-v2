#!/bin/bash
echo " "
echo " "
echo "<<<<<<<<<<< Installing requirements >>>>>>>>>>>>>>"

echo " "
source $(pipenv --venv)/bin/activate
pipenv install

echo "<<<<<<<<<<< Export variable environment >>>>>>>>>>>>>>"


export SECRET_KEY=$sec_key
export DB_NAME=$db_name
export DB_HOST=$db_host
export DB_PASSWORD=$db_password
export DB_USER=$db_user


echo "<<<<<<<<<<< Export variable environment >>>>>>>>>>>>>>"

echo " "
echo " "
echo ‘'<<<<<<<<<<<<<<' Run migration '>>>>>>>>>>>>>>>>>>>>>>>'’

echo " "
pipenv run python manage.py migrate

echo " "
echo " "
echo ‘'<<<<<<<<<<<<<<' Run collectistatic '>>>>>>>>>>>>>>>>>>>>>>>'’

echo " "
pipenv run python manage.py collectstatic

echo " "
echo " "
echo "<<<<<<<<<<<<<< Restarting gunicorn >>>>>>>>>>>>>>>>>>>>"
echo "$user_password" | sudo -S systemctl restart gunicorn

echo " "
echo " "
echo "<<<<<<<<<<<<<<<< Restarting nginx >>>>>>>>>>>>>>>>>>>>>>"
echo " "

echo "$user_password" | sudo -S systemctl restart nginx

echo " "
echo " "
echo "<<<<<<<<<< started server. ending SSH session >>>>>>>>>>"

echo ‘'<<<<<<<<<<<<<<' Starting redis '>>>>>>>>>>>>>>>>>>>>>>>'’
echo " "
echo "$user_password" | sudo -S systemctl restart redis

echo " "
echo " "
echo ‘'<<<<<<<<<<<<<<' Starting celery '>>>>>>>>>>>>>>>>>>>>>>>'’
echo " "
echo "$user_password" | sudo -S systemctl restart celery
exit

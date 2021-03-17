#!/bin/bash

rm -rf checklistapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations checklistapi
python manage.py migrate checklistapi
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata my_users
python manage.py loaddata tasks

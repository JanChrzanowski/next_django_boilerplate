#!/bin/sh

echo "Making migrations..."
python manage.py makemigrations --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating admin..."
python manage.py create_admin

echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000

#!/bin/bash

rm db.sqlite3
rm -rf ./restaurantapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations restaurantapi
python3 manage.py migrate restaurantapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata locations
python3 manage.py loaddata restaurants
python3 manage.py loaddata ratings
python3 manage.py loaddata reviews

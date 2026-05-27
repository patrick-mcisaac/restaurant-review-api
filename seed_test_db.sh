#!/bin/bash

rm test_db.sqlite3
rm -rf ./restaurantapi/migrations
pipenv run python3 manage.py makemigrations restaurantapi --settings=restaurantproject.settings.test
pipenv run python3 manage.py migrate --settings=restaurantproject.settings.test
# pipenv run python3 manage.py migrate restaurantapi --settings=restaurantproject.settings.test
pipenv run python3 manage.py loaddata users --settings=restaurantproject.settings.test
pipenv run python3 manage.py loaddata tokens --settings=restaurantproject.settings.test
pipenv run python3 manage.py loaddata cities --settings=restaurantproject.settings.test
pipenv run python3 manage.py loaddata restaurants --settings=restaurantproject.settings.test
pipenv run python3 manage.py loaddata restaurant_locations --settings=restaurantproject.settings.test
pipenv run python3 manage.py loaddata experiences --settings=restaurantproject.settings.test

pipenv run python3 manage.py loaddata reviews --settings=restaurantproject.settings.test
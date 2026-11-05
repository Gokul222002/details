#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

cd ProjectDjango/mylist
python manage.py collectstatic --no-input
python manage.py migrate

#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Prepare static files and run database migrations
python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser using environment variables if CREATE_SUPERUSER is set
if [ "$CREATE_SUPERUSER" ]; then
    # --no-input uses DJANGO_SUPERUSER_USERNAME, EMAIL, and PASSWORD
    # || true prevents the build from failing if the user already exists
    python manage.py createsuperuser --no-input || true
fi
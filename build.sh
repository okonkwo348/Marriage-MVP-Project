#!/usr/bin/env bash
set -o errexit

# Install dependencies without --user
pip install -r requirements.txt

# Collect static files and apply migrations
python manage.py collectstatic --no-input
python manage.py migrate
#!/usr/bin/env bash
set -o errexit

# Install dependencies
pip install -r requirements.txt --user

# Collect static files and apply migrations
python manage.py collectstatic --no-input
python manage.py migrate
#!/bin/sh

set -eu

if [ -f .env ]; then
    set -a
    . ./.env
    set +a
fi

: "${DJANGO_SUPERUSER_USERNAME:?DJANGO_SUPERUSER_USERNAME is required}"
: "${DJANGO_SUPERUSER_PASSWORD:?DJANGO_SUPERUSER_PASSWORD is required}"
: "${DJANGO_SUPERUSER_EMAIL:?DJANGO_SUPERUSER_EMAIL is required}"

# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python manage.py migrate --noinput

python manage.py shell -c "
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ['DJANGO_SUPERUSER_USERNAME']
email = os.environ['DJANGO_SUPERUSER_EMAIL']
password = os.environ['DJANGO_SUPERUSER_PASSWORD']

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
"

exec "$@"

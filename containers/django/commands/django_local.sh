#!/bin/sh

set -o errexit
set -e pipefail
set -o nounset

python manage.py makemigrations
python manage.py migrate

tail -f /dev/null

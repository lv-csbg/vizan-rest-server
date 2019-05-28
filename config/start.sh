#!/bin/bash
set -e

#####
# Django setup
#####

# Django: migrate
#
# Django will see that the tables for the initial migrations already exist
# and mark them as applied without running them. (Django won’t check that the
# table schema match your models, just that the right table names exist).
echo "==> Django setup, executing: migrate"
python3 /srv/${DJANGO_PROJECT_NAME}/manage.py migrate --fake-initial

# Django: collectstatic
echo "==> Django setup, executing: collectstatic"
python3 /srv/${DJANGO_PROJECT_NAME}/manage.py collectstatic --noinput -v 3


#####
# Start uWSGI
#####
echo "==> Starting uWSGI ..."
/usr/local/bin/uwsgi --emperor /etc/uwsgi/django-uwsgi.ini

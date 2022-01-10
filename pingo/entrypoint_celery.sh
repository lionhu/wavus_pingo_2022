#!/bin/sh

echo "Wating for postgres to startup ..."
#wait unting postgres container started up
python3 manage.py wait_for_db


echo "Check postgres to startup ..."
while ! nc -z postgres 5432; do sleep 2; done

echo "Starting supervisord..."
sleep 5;supervisord -c /etc/supervisord_celery.conf

exec "$@"

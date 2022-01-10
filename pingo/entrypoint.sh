#!/bin/sh
echo "Wating for postgres to startup ..."
#wait unting postgres container started up
python3 manage.py wait_for_db

echo "Starting supervisord..."
supervisord -c /etc/supervisord.conf

exec "$@"

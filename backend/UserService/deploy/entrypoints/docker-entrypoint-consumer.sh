#!/bin/sh
cd $WORK_DIR

echo "Run service"
while true; do
    python manage.py consumers
done

exec "$@"
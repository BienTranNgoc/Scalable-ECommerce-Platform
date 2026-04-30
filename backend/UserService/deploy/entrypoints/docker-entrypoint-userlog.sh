#!/bin/sh
cd $WORK_DIR

echo "Run service"
while true; do
    python manage.py user_log_consumer
done

exec "$@"
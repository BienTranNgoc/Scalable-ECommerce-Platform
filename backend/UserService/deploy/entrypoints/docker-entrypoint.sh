#!/bin/sh
cd $WORK_DIR

echo "Collect static files"
python manage.pyc collectstatic --noinput

# Start server
echo "Starting server"
uwsgi --ini deploy/uwsgi/uwsgi.ini

#!/bin/bash
# Collect static files
echo "Collect static files"
python manage.pyc collectstatic --noinput

# Start server
echo "Starting server"
uwsgi --ini uwsgi.ini

# Here the received command is executed
exec "$@"

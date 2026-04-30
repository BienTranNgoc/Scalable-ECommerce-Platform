#!/bin/bash
# When starting the django app container, we need to wait until the postgress DB is ready to receive connections
# docker-compose "depends_on: - db" checks the container started, but is not enough to check that the database is ready to take connections
# This script also accepts a command to be executed after the DB is ready (i.e. migrate, runserver or a script..)

# Function to check the health of the MySQL database
#function mysql_ready(){
#python3 << END
#import sys
#import pymysql
#try:
#	print("Trying to connect database '$DB_DEFAULT_NAME' on host '$DB_DEFAULT_HOST' ..")
#	cnx = pymysql.connect(user='${DB_DEFAULT_USER}', password='${DB_DEFAULT_PASSWORD}', host='${DB_DEFAULT_HOST}', database='${DB_DEFAULT_NAME}')
#	cnx.close()
#except pymysql.err.OperationalError as e:
#	print(e)
#	sys.exit(-1)
#sys.exit(0)
#END
#}
#until mysql_ready; do
#  >&2 echo "MySQL is unavailable - sleeping"
#  sleep 1
#done

>&2 echo "Mysql is up - continuing..."

echo "Run service"
while true; do
    python manage.py user_log_consumer
done

# Here the received command is executed
exec "$@"
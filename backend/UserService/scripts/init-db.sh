#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status.

# Ensure required environment variables are set
# REQUIRED_ENV_VARS=("DB_DEFAULT_HOST" "DB_DEFAULT_PORT" "DB_DEFAULT_USER" "DB_DEFAULT_PASSWORD" "DB_DEFAULT_NAME")
# for var in "${REQUIRED_ENV_VARS[@]}"; do
#     if [ -z "${!var}" ]; then
#         echo "Error: Environment variable $var is not set."
#         exit 1
#     fi
# done

# Wait for database to be ready
# echo "Waiting for database to be ready..."
# max_tries=30
# count=0
# while ! mysqladmin ping -h"$DB_DEFAULT_HOST" -P"$DB_DEFAULT_PORT" -u"$DB_DEFAULT_USER" -p"$DB_DEFAULT_PASSWORD" --silent; do
#     sleep 3
#     count=$((count + 1))
#     if [ $count -gt $max_tries ]; then
#         echo "Error: Could not connect to database after $max_tries attempts."
#         exit 1
#     fi
# done

# Run migrations
echo "Running database makemigrations..."
python manage.py makemigrations
sleep 5
echo "Running database migrations..."
python manage.py migrate

# Import all SQL dumps from the database folder
# if [ -d "database" ]; then
#     echo "Importing SQL dumps..."
#     for sql_file in database/*.sql; do
#         if [ -f "$sql_file" ]; then
#             echo "Importing $sql_file..."
#             mysql -h"$DB_DEFAULT_HOST" -P"$DB_DEFAULT_PORT" -u"$DB_DEFAULT_USER" -p"$DB_DEFAULT_PASSWORD" "$DB_DEFAULT_NAME" < "$sql_file" || {
#                 echo "Error: Failed to import $sql_file"
#                 exit 1
#             }
#         fi
#     done
# else
#     echo "Warning: 'database' folder not found. Skipping SQL import."
# fi

# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:$APP_PORT
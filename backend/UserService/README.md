# BusinessResourceManagement
## Setup pipeline
1. docker network create business-resource-network
2. docker run --name mysql-dev \
  --network business-resource-network \
  -e MYSQL_ROOT_PASSWORD=business_resource_password \
  -e MYSQL_DATABASE=business_resource_db \
  -e MYSQL_USER=business_resource_user \
  -e MYSQL_PASSWORD=business_resource_password \
  -p 3306:3306 \
  -d mysql:8.0.35 \
  --character-set-server=utf8mb4 \
  --collation-server=utf8mb4_unicode_ci

3. python -m venv venv
4. source venv/Scripts/activate
5. python manage.py makemigrations
6. python manage.py migrate
7. python manage.py runserver
8. python manage.py consumers (open new terminal)

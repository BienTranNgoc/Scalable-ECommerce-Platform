docker pull mysql:latest
docker run --name mysql-dev -e MYSQL_ROOT_PASSWORD=duytp123 -d mysql:latest
docker exec -it db mysql -uroot -p

docker build --target deploy --tag harbor-beta.fcam.vn/backend/servicemngtb2b .
docker push harbor-beta.fcam.vn/backend/servicemngtb2b
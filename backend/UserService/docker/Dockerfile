FROM python:3.10.14-bullseye AS base
RUN mkdir -p /mnt
RUN mkdir -p /mnt/src
WORKDIR /mnt/src
COPY requirements.txt /mnt/src/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends default-libmysqlclient-dev gcc
RUN apt-get install -y python3-pymysql
RUN pip install --upgrade pip
RUN pip install -r base.txt
RUN mkdir -p logs/
RUN mkdir -p logs/face/
RUN chmod 777 -R logs/
COPY . .

# FROM base AS test
# COPY ./docker-entrypoints/docker-entrypoint.sh /docker-entrypoint.sh
# RUN chmod a+x /docker-entrypoint.sh
# ENTRYPOINT ["/docker-entrypoint.sh"]
FROM base AS evaluation_face
COPY ./docker/docker-entrypoints/docker-entrypoint-evaluation-face-result.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

FROM base AS check_file_export
COPY ./docker/docker-entrypoints/docker-entrypoint-check-file-export.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

FROM base AS check_face_result
COPY ./docker/docker-entrypoints/docker-entrypoint-check-service-health.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

FROM base AS deploy
COPY ./docker/docker-entrypoints/docker-entrypoint-deploy.sh /docker-entrypoint.sh
RUN pip install uwsgi
EXPOSE 9000

RUN python -m compileall -b .
RUN find . -maxdepth 4 -name "*.py" -not -path "./*/local_settings.py" -not -path "./*/*/migrations/*" -not -path "./*/*/migrations/__init__.py" -delete
RUN chmod a+x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

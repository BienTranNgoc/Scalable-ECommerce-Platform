FROM python:3.12.3-bullseye AS base
# Set work directory
RUN mkdir -p /mnt
RUN mkdir -p /mnt/UserService
WORKDIR /mnt/BusinessResourceManagement
COPY requirements/base.txt /mnt/BusinessResourceManagement/requirements.txt
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    default-mysql-client \
    libpq-dev \
    python3-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install -r base.txt
# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# ENV APP_PORT=9000
# ENV DJANGO_SETTINGS_MODULE=UserService.settings.base
# Create directory for logs
RUN mkdir -p logs
RUN chmod 777 -R logs/
# Copy project files
COPY . .
# --- DEPLOY STAGE ---
FROM base AS consumer
COPY ./docker-entrypoints/docker-entrypoint-consumer.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

# --- DEPLOY USER LOG STAGE ---
FROM base AS userlog
COPY ./docker-entrypoints/docker-entrypoint-userlog.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

FROM base AS deploy
COPY ./docker-entrypoints/docker-entrypoint-deploy.sh /docker-entrypoint.sh
RUN pip install uwsgi
EXPOSE 9000

RUN python -m compileall -b .
RUN find . -maxdepth 4 -name "*.py" -not -path "./*/local_settings.py" -not -path "./*/*/migrations/*" -not -path "./*/*/migrations/__init__.py" -delete
RUN chmod a+x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
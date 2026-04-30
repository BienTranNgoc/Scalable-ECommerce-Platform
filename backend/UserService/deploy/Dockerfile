FROM python:3.10.14-bullseye AS base

# Set work directory
RUN mkdir -p /opt/app
WORKDIR /opt/app
ENV WORK_DIR=/opt/app
COPY requirements/base.txt ./requirements.txt

# ========== DEVELOPER =============
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
RUN pip install --upgrade pip  \
    && pip install -r requirements.txt \
    && pip install uwsgi
RUN mkdir -p logs \
    && chmod 777 -R logs/
# Copy project files
COPY . .

EXPOSE 8080
RUN python -m compileall -b .
RUN find . -maxdepth 4 -name "*.py" -not -path "./*/local_settings.py" -not -path "./*/*/migrations/*" -not -path "./*/*/migrations/__init__.py" -delete

# ================ END =============

RUN chmod -R a+x /opt/app/deploy/entrypoints
RUN chmod -R a+x /opt/app/deploy/entrypoint.sh
ENTRYPOINT ["/opt/app/deploy/entrypoint.sh"]
# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

# Creating a python base with shared environment variables
FROM python:3.12.2-bookworm

# Устанавливаем необходимые зависимости для Poetry
RUN buildDeps="build-essential curl vim tar" \
    && apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends $buildDeps

# Устанавливаем Poetry
# Вы можете заменить версию Poetry, указав конкретную версию после "@"
RUN curl -sSL https://install.python-poetry.org | python3 -

# Добавляем директорию bin Poetry в PATH, чтобы можно было запускать Poetry из любого места
ENV PATH="/root/.local/bin:$PATH"

# Очистка кеша apt для уменьшения размера образа
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

ARG VENV_HASH
ARG ACCESS_TOKEN
ARG BOT_TOKEN
ARG JWT_SECRET
ARG S3_ACCESS_KEY_ID
ARG S3_SECRET_ACCESS_KEY
ARG DATABASE_URI
ARG SENTRY_DSN
ARG JWT_ACCESS_TOKEN_EXPIRE_SECONDS
ARG JWT_REFRESH_TOKEN_EXPIRE_SECONDS
ARG REDIS_NOTIFIER_URL
ARG S3_PHOTO_BUCKET_NAME

ENV WORKERS=$WORKERS_COUNT
ENV BOT_TOKEN=$BOT_TOKEN
ENV JWT_SECRET=$JWT_SECRET
ENV S3_ACCESS_KEY_ID=$S3_ACCESS_KEY_ID
ENV S3_SECRET_ACCESS_KEY=$S3_SECRET_ACCESS_KEY
ENV DATABASE_URI=$DATABASE_URI
ENV SENTRY_DSN=$SENTRY_DSN
ENV JWT_ACCESS_TOKEN_EXPIRE_SECONDS=$JWT_ACCESS_TOKEN_EXPIRE_SECONDS
ENV JWT_REFRESH_TOKEN_EXPIRE_SECONDS=$JWT_REFRESH_TOKEN_EXPIRE_SECONDS
ENV REDIS_NOTIFIER_URL=$REDIS_NOTIFIER_URL
ENV S3_PHOTO_BUCKET_NAME=$S3_PHOTO_BUCKET_NAME

COPY ./api/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
WORKDIR /api
COPY ./api/pyproject.toml ./api/poetry.lock ./
COPY ./api/src/ ./src/

RUN poetry config virtualenvs.create true \
 && poetry config virtualenvs.in-project true \
 && poetry install --only main

EXPOSE 8080
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD alembdic upgrad heads
CMD gunicorn src.main:api --workers $WORKERS -k uvicorn.workers.UvicornWorker --bind unix:/tmp/api.sock



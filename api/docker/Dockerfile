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
ARG WORKERS_COUNT=3
ENV WORKERS=$WORKERS_COUNT

RUN echo $WORKERS

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
CMD gunicorn src.main:api --workers $WORKERS -k uvicorn.workers.UvicornWorker --bind unix:api.sock



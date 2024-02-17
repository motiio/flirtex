# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

# Creating a python base with shared environment variables
FROM python:3.12.2-bookworm as python-base
ARG WORKERS_COUNT

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
    CACHED_API_VENV="/usr/local/src/flirtex/env/api/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# builder-base is used to build dependencies
FROM python-base AS builder-base
RUN buildDeps="build-essential curl vim" \
    && apt-get update \
    && apt-get install -y --no-install-recommends $buildDeps \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.7.0
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 - --version ${POETRY_VERSION}

# Copying Python requirements for caching
WORKDIR $PYSETUP_PATH
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main

# 'prod' stage installs all dev deps and can be used to develop code.
FROM python-base as 'prod'
ENV FASTAPI_ENV=production

# Copying poetry and venv into image
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY $CACHED_API_VENV $VENV_PATH

# Copying in our entrypoint
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Set working directory and copy source code
WORKDIR /api
COPY ./src/ ./src/

EXPOSE 8080
# Define entrypoint and default command
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD alembic upgrade head
CMD gunicorn src.main:api --workers $WORKERS_COUNT -k uvicorn.workers.UvicornWorker --bind unix:/tmp/api.sock


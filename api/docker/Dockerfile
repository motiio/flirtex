# Dockerfile
# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

# Creating a python base with shared environment variables
FROM flirtex.registry.jetbrains.space/p/connecta/containers/3.12.2-poetry:latest

ARG VENV_HASH
ARG ACCESS_TOKEN
ARG WORKERS=3

RUN curl -f -L -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://files.pkg.jetbrains.space/flirtex/p/connecta/default-automation-caches/caches/backend/poetry-$VENV_HASH.tar.gz" \
  | tar -xz -C .venv

WORKDIR /api
COPY pyproject.toml poetry.lock ./
COPY ./src/ ./src/

RUN poetry config virtualenvs.create true \
 && poetry config virtualenvs.in-project true \
 && poetry install --only main

EXPOSE 8080

CMD ["gunicorn", "src.main:api", "--workers", "$WORKERS", "-k", "uvicorn.workers.UvicornWorker", "--bind", "unix:api.sock"]


#!/bin/sh

set -e

# activate our virtual environment here
. /opt/pysetup/.venv/bin/activate

# You can put other setup logic here

# Если скрипту передана команда (например, bash для отладки),
# выполнить переданную команду вместо запуска gunicorn:
if [ "$1" ]; then
  exec "$@"
else
  # Выполнение миграций
  alembic upgrade head
  # Запуск Gunicorn
  exec gunicorn src.main:api --workers ${WORKERS_COUNT:-4} -k uvicorn.workers.UvicornWorker --bind unix:/tmp/api.sock
fi

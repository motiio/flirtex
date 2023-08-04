import os
import sys

# Получаем путь к директории "src" в вашем проекте
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))

# Добавляем путь к "src" в переменную окружения PYTHONPATH
sys.path.insert(0, src_path)
import shutil
from pathlib import Path

import pytest


@pytest.fixture(scope="session", autouse=True)
def remove_pycache():
    pycache_dirs = list(Path(".").rglob("__pycache__"))
    for pycache_dir in pycache_dirs:
        shutil.rmtree(pycache_dir)

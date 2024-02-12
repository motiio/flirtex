job("[PROD]. API deploy") {
    startOn {}

    container(displayName = "Build with Poetry", image = "flirtex.registry.jetbrains.space/p/connecta/containers/3.12.2-poetry:latest") {
        cache {
            // Генерация имени файла кэша
            // Использование хэша файла pyproject.toml гарантирует, что все запуски задач с
            // одинаковым pyproject.toml будут использовать кэшированные зависимости
            storeKey = "poetry-{{ hashFiles('api/pyproject.toml') }}"

            // Вариант восстановления
            // Если нужный файл кэша не найден, использовать кэш из 'poetry-master.tar.gz'
            restoreKeys {
                +"poetry-master"
            }

            // Локальный путь к директории файла кэша
            localPath = ".venv"
        }

        shellScript {
            content = """
            poetry config virtualenvs.create false
            poetry install
            """
        }
    }

    parameters {
        text("env", value = "prod") {
            options("dev", "prod")
        }
    }



    host("Start deployment API to TEST server") {
        shellScript {
            content = """
            pwd
            """
        }
    requirements {
         workerTags("ProdPool-1")
        }
    }
}


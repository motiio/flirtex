job("[PROD]. API deploy") {
    startOn {}
    parameters {
        text("VENV_HASH", value = "poetry-{{ hashFiles('api/pyproject.toml') }}")

        text("ENVIRONMENT", value = "prod") {
            options("dev", "prod")
        }
        
        text("MAJAOR_V", value = "0")
        text("MINOR_V", value = "0")
    }
    container(displayName = "Testing...", image = "flirtex.registry.jetbrains.space/p/connecta/containers/3.12.2-poetry:latest") {
        cache {
            // Генерация имени файла кэша
            // Использование хэша файла pyproject.toml гарантирует, что все запуски задач с
            // одинаковым pyproject.toml будут использовать кэшированные зависимости
            storeKey = "{{VENV_HASH}}"

            // Вариант восстановления
            // Если нужный файл кэша не найден, использовать кэш из 'poetry-master.tar.gz'
            restoreKeys {
                +"poetry-master"
            }

            // Локальный путь к директории файла кэша
            localPath = "api/.venv"
        }

        shellScript {
            content = """
            cd api
            poetry config virtualenvs.create true
            poetry config virtualenvs.in-project true
            poetry install --no-root
            poetry run pytest --cov=src --cov-report=term --cov-config=.coveragerc
            """
        }
    }

    host("Building...") {
        dockerBuildPush {
            // path to Docker context (by default, context is working dir)
            context = "api/docker"
            // path to Dockerfile relative to the project root
            // if 'file' is not specified, Docker will look for it in 'context'/Dockerfile
            file = "Dockerfile"
            // build-time variables
            args["VENV_HASH"] = "{{ VENV_HASH }}"
            args["ACCESS_TOKEN"] = "{{ project::API_CACHE_ACCESS_TOKEN }}"
            // image labels
            labels["vendor"] = "flirtex"
            tags {
                // use current job run number as a tag - '0.0.run_number'
                +"flirtex.registry.jetbrains.space/p/connecta/containers/api:{{ MAJAOR_V }}.{{ MINOR_V }}.${"$"}JB_SPACE_EXECUTION_NUMBER"
            }
        }
        requirements {
            workerTags("ProdPool-1")
        }
    }
}


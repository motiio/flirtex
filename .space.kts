job("[PROD]. API deploy") {
    startOn {}
    parameters {
        text("VENV_HASH", value = "poetry-{{ hashFiles('api/pyproject.toml') }}")
        text("ENVIRONMENT", value = "PROD") {
            options("DEV", "PROD")
        }
        text("MAJAOR_V", value = "0")
        text("MINOR_V", value = "0")
    }
    host(displayName = "Setup parameters") {
        kotlinScript { api ->
            val env = api.parameters["ENVIRONMENT"]
            when (env) {
                "PROD" -> {
                    // secrets
                    api.secrets["BOT_TOKEN"] = Ref("project:PROD__BOT_TOKEN")

                    api.secrets["JWT_SECRET"] = Ref("project:PROD__JWT_SECRET")

                    api.secrets["S3_ACCESS_KEY_ID"] = Ref("project:PROD__S3_ACCESS_KEY_ID")
                    api.secrets["S3_SECRET_ACCESS_KEY"] = Ref("project:PROD__S3_SECRET_ACCESS_KEY")

                    api.secrets["DATABASE_URI"] = Ref("project:PROD__DATABASE_URI")

                    api.secrets["SENTRY_DSN"] = Ref("project:PROD__SENTRY_DSN")

                    // params

                    api.parameters["JWT_ACCESS_TOKEN_EXPIRE_SECONDS"] = Ref("project:PROD__JWT_ACCESS_TOKEN_EXPIRE_SECONDS")
                    api.parameters["JWT_REFRESH_TOKEN_EXPIRE_SECONDS"] = Ref("project:PROD__JWT_ACCESS_TOKEN_EXPIRE_SECONDS")
                    api.parameters["REDIS_NOTIFIER_URL"] = Ref("project:PROD__REDIS_NOTIFIER_URL")
                    api.parameters["S3_PHOTO_BUCKET_NAME"] = Ref("project:PROD__S3_PHOTO_BUCKET_NAME")
                    api.parameters["WORKERS_COUNT"] = Ref("project:PROD__WORKERS_COUNT")
                }

                "DEV" -> {
                    // secrets
                    api.parameters["BOT_TOKEN"] = Ref("project:DEV__BOT_TOKEN")

                    api.parameters["JWT_SECRET"] = Ref("project:DEV__JWT_SECRET")

                    api.parameters["S3_ACCESS_KEY_ID"] = Ref("project:DEV__S3_ACCESS_KEY_ID")
                    api.parameters["S3_SECRET_ACCESS_KEY"] = Ref("project:DEV__S3_SECRET_ACCESS_KEY")

                    api.parameters["DATABASE_URI"] = Ref("project:DEV__DATABASE_URI")

                    api.parameters["SENTRY_DSN"] = Ref("project:DEV__SENTRY_DSN")

                    // params

                    api.parameters["JWT_ACCESS_TOKEN_EXPIRE_SECONDS"] = Ref("project:DEV__JWT_ACCESS_TOKEN_EXPIRE_SECONDS")
                    api.parameters["JWT_REFRESH_TOKEN_EXPIRE_SECONDS"] = Ref("project:DEV__JWT_ACCESS_TOKEN_EXPIRE_SECONDS")
                    api.parameters["REDIS_NOTIFIER_URL"] = Ref("project:DEV__REDIS_NOTIFIER_URL")
                    api.parameters["S3_PHOTO_BUCKET_NAME"] = Ref("project:DEV__S3_PHOTO_BUCKET_NAME")
                    api.parameters["WORKERS_COUNT"] = Ref("project:DEV__WORKERS_COUNT")
                }
            }

        }
    }
    container(displayName = "Testing...", image = "flirtex.registry.jetbrains.space/p/connecta/containers/3.12.2-poetry:latest") {
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

    kaniko {
        build {
            file = "./api/docker/Dockerfile"
            labels["vendor"] = "flirtex"
            args["BOT_TOKEN"] = "{{ BOT_TOKEN }}"
            args["JWT_SECRET"] = "{{ JWT_SECRET }}"
            args["S3_ACCESS_KEY_ID"] = "{{ S3_ACCESS_KEY_ID }}"
            args["S3_SECRET_ACCESS_KEY"] = "{{ S3_SECRET_ACCESS_KEY }}"
            args["DATABASE_URI"] = "{{ DATABASE_URI }}"
            args["SENTRY_DSN"] = "{{ SENTRY_DSN }}"
            args["JWT_ACCESS_TOKEN_EXPIRE_SECONDS"] = "{{ JWT_ACCESS_TOKEN_EXPIRE_SECONDS }}"
            args["JWT_REFRESH_TOKEN_EXPIRE_SECONDS"] = "{{ JWT_REFRESH_TOKEN_EXPIRE_SECONDS }}"
            args["REDIS_NOTIFIER_URL"] = "{{ REDIS_NOTIFIER_URL }}"
            args["S3_PHOTO_BUCKET_NAME"] = "{{ S3_PHOTO_BUCKET_NAME }}"
            args["WORKERS_COUNT"] = "{{ WORKERS_COUNT }}"
        }
        push("flirtex.registry.jetbrains.space/p/connecta/containers/api") {
            tags {
                // use current job run number as a tag - '0.0.run_number'
                +"{{ MAJAOR_V }}.{{ MINOR_V }}.${"$"}JB_SPACE_EXECUTION_NUMBER"
                +"latest"
            }

        }
    }
    host(displayName = "Restarting app..."){
        shellScript {
            content = """
                docker-compose pull api
                docker-compose up -d api
            """
        }
    }
}


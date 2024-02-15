job("API Tests") {
    startOn {}


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
}

job("API Build and deploy") {

    startOn {}
    parameters {
        text("ENVIRONMENT", value = "PROD") {
            options("DEV", "PROD")
        }
        text("MAJOR_V", value = "0")
        text("MINOR_V", value = "0")
    }

    container(displayName = "Testing...", image = "flirtex.registry.jetbrains.space/p/connecta/containers/3.12.2-poetry:latest") {
//        cache {
        // Генерация имени файла кэша
        // Использование хэша файла pyproject.toml гарантирует, что все запуски задач с
        // одинаковым pyproject.toml будут использовать кэшированные зависимости
//            storeKey = "poetry-{{ hashFiles('api/pyproject.toml') }}"

        // Вариант восстановления
        // Если нужный файл кэша не найден, использовать кэш из 'poetry-master.tar.gz'
//            restoreKeys {
//                +"poetry-master"
//            }

        // Локальный путь к директории файла кэша
//            localPath = "api/.venv"
//        }

//        shellScript {
//            content = """
//            cd api
//            poetry config virtualenvs.create true
//            poetry config virtualenvs.in-project true
//            poetry install --no-root
//            poetry run pytest --cov=src --cov-report=term --cov-config=.coveragerc
//            """
//        }
        fileArtifacts {
            localPath = "api/"
            // Fail job if build/publish/app/ is not found
            optional = false
            remotePath = "api.gz"
            archive = true
            onStatus = OnStatus.SUCCESS
        }
    }

    host(displayName = "Create job parameters") {
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
                    api.secrets["DEPLOY_PK"] = Ref("project:PROD__DEPLOY_PK")

                    // params
                    api.parameters["JWT_ACCESS_TOKEN_EXPIRE_SECONDS"] = Ref("project:PROD__JWT_ACCESS_TOKEN_EXPIRE_SECONDS")
                    api.parameters["JWT_REFRESH_TOKEN_EXPIRE_SECONDS"] = Ref("project:PROD__JWT_ACCESS_TOKEN_EXPIRE_SECONDS")
                    api.parameters["REDIS_NOTIFIER_URL"] = Ref("project:PROD__REDIS_NOTIFIER_URL")
                    api.parameters["S3_PHOTO_BUCKET_NAME"] = Ref("project:PROD__S3_PHOTO_BUCKET_NAME")
                    api.parameters["WORKERS_COUNT"] = Ref("project:PROD__WORKERS_COUNT")

                    api.parameters["SSH_PORT"] = Ref("project:PROD__SSH_PORT")
                    api.parameters["SSH_HOST"] = Ref("project:PROD__SSH_HOST")
                    api.parameters["SSH_USER"] = Ref("project:PROD__SSH_USER")
                }

                "DEV" -> {
                    // secrets
                    api.secrets["BOT_TOKEN"] = Ref("project:DEV__BOT_TOKEN")

                    api.secrets["JWT_SECRET"] = Ref("project:DEV__JWT_SECRET")

                    api.secrets["S3_ACCESS_KEY_ID"] = Ref("project:DEV__S3_ACCESS_KEY_ID")
                    api.secrets["S3_SECRET_ACCESS_KEY"] = Ref("project:DEV__S3_SECRET_ACCESS_KEY")

                    api.secrets["DATABASE_URI"] = Ref("project:DEV__DATABASE_URI")

                    api.secrets["SENTRY_DSN"] = Ref("project:DEV__SENTRY_DSN")

                    api.secrets["DEPLOY_PK"] = Ref("project:DEV__DEPLOY_PK")

                    // params

                    api.parameters["JWT_ACCESS_TOKEN_EXPIRE_SECONDS"] = Ref("project:DEV__JWT_ACCESS_TOKEN_EXPIRE_SECONDS")
                    api.parameters["JWT_REFRESH_TOKEN_EXPIRE_SECONDS"] = Ref("project:DEV__JWT_ACCESS_TOKEN_EXPIRE_SECONDS")
                    api.parameters["REDIS_NOTIFIER_URL"] = Ref("project:DEV__REDIS_NOTIFIER_URL")
                    api.parameters["S3_PHOTO_BUCKET_NAME"] = Ref("project:DEV__S3_PHOTO_BUCKET_NAME")
                    api.parameters["WORKERS_COUNT"] = Ref("project:DEV__WORKERS_COUNT")

                    api.parameters["SSH_PORT"] = Ref("project:DEV__SSH_PORT")
                    api.parameters["SSH_HOST"] = Ref("project:DEV__SSH_HOST")
                    api.parameters["SSH_USER"] = Ref("project:DEV__SSH_USER")
                }
            }

        }
    }
    host(displayName = "Run deploy script") {

        env["SSH_HOST"] = "{{ SSH_HOST }}"
        env["SSH_PORT"] = "{{ SSH_PORT }}"
        env["SSH_USER"] = "{{ SSH_USER }}"
        env["DEPLOY_PK"] = "{{ DEPLOY_PK }}"
        fileInput {
            source = FileSource.FileArtifact(
                    "{{ run:file-artifacts.default-repository }}/{{ run:file-artifacts.default-base-path }}",
                    "api.gz",
                    extract = true
            )
            localPath = "./services/"
        }

        shellScript {
            content = """
                    echo ${'$'}DEPLOY_PK | base64 --decode > id_rsa
                    chmod 400 id_rsa
                    mkdir -p ~/.ssh/known_hosts
                    ssh-keyscan -p ${'$'}SSH_PORT ${'$'}SSH_HOST >> ~/.ssh/known_hosts
                    scp -i id_rsa \
                        -P ${'$'}SSH_PORT \
                        -r ./api/* \
                        ${'$'}SSH_USER@${'$'}SSH_HOST:/usr/local/src/flirtex/api/
              """
        }
        requirements {
            workerTags("ProdPool-1")
        }
    }
}


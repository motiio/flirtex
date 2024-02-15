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
                    api.secrets["CACHE_ACCESS_KEY"] = Ref("project:PROD__CACHE_ACCESS_KEY")
                    api.secrets["ARTIFACTS_ACCESS_KEY"] = Ref("project:PROD__ARTIFACTS_ACCESS_KEY")

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
                    api.secrets["CACHE_ACCESS_KEY"] = Ref("project:DEV__CACHE_ACCESS_KEY")
                    api.secrets["ARTIFACTS_ACCESS_KEY"] = Ref("project:DEV__ARTIFACTS_ACCESS_KEY")

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
    host(displayName = "Deploying...") {

        env["SSH_HOST"] = "{{ SSH_HOST }}"
        env["SSH_HOST"] = "{{ SSH_HOST }}"
        env["SSH_PORT"] = "{{ SSH_PORT }}"
        env["SSH_USER"] = "{{ SSH_USER }}"
        env["DEPLOY_PK"] = "{{ DEPLOY_PK }}"
        env["CACHE_ACCESS_KEY"] = "{{ CACHE_ACCESS_KEY }}"
        env["ARTIFACTS_ACCESS_KEY"] = "{{ ARTIFACTS_ACCESS_KEY }}"
        env["VENV_HASH"] = "poetry-{{ hashFiles('api/pyproject.toml') }}"
        env["ARTIFACTS_PATH"] = "{{ run:file-artifacts.default-repository }}/{{ run:file-artifacts.default-base-path }}/api.gz"

        shellScript {
            content = """
                    echo ${'$'}DEPLOY_PK | base64 --decode > id_rsa
                    chmod 400 id_rsa
                    ssh-keyscan -p ${'$'}SSH_PORT ${'$'}SSH_HOST >> ./known_hosts
                    echo Start downloading hash ${'$'}VENV_HASH.tar.gz
                    echo Start downloading artifacts ${'$'}ARTIFACTS_PATH
                    ssh -i id_rsa \
                        -o UserKnownHostsFile=/dev/null \
                        -o StrictHostKeyChecking=no \
                        -o LogLevel=INFO \
                        -p ${'$'}SSH_PORT
                        ${'$'}SSH_USER@${'$'}SSH_HOST "\
                        rm -rf /usr/local/src/flirtex/api/
                        mkdir -p /usr/local/src/flirtex/api/
                        echo Start downloading hash ${'$'}VENV_HASH.tar.gz
                        curl -f -L \
                            -H 'Authorization: Bearer ${'$'}CACHE_ACCESS_KEY' \
                            https://files.pkg.jetbrains.space/flirtex/p/connecta/default-automation-caches/caches/backend/${'$'}VENV_HASH.tar.gz \
                            --output '/usr/local/src/flirtex/'
                        echo Start downloading artifacts ${'$'}ARTIFACTS_PATH
                        curl -f -L \
                            -H 'Authorization: Bearer ${'$'}ARTIFACTS_ACCESS_KEY' \
                            https://files.pkg.jetbrains.space/flirtex/p/connecta/${'$'}ARTIFACTS_PATH \
                            --output '/usr/local/src/flirtex/'"
                    scp -i id_rsa \
                        -o UserKnownHostsFile=/dev/null \
                        -o StrictHostKeyChecking=no \
                        -P ${'$'}SSH_PORT \
                        -r ./docker-compose.yml \
                        ${'$'}SSH_USER@${'$'}SSH_HOST:/usr/local/src/flirtex/
              """
        }
        requirements {
            workerTags("ProdPool-1")
        }
    }
}


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
        text("ENVIRONMENT", value = "PROD")
        text("MAJOR_V", value = "0")
        text("MINOR_V", value = "0")
    }

    container(displayName = "Testing...", image = "flirtex.registry.jetbrains.space/p/connecta/containers/3.12.2-poetry:latest") {
        cache {
//         Генерация имени файла кэша
//         Использование хэша файла pyproject.toml гарантирует, что все запуски задач с
//         одинаковым pyproject.toml будут использовать кэшированные зависимости
            storeKey = "poetry-{{ hashFiles('api/pyproject.toml') }}"
//         Вариант восстановления
//         Если нужный файл кэша не найден, использовать кэш из 'poetry-master.tar.gz'
            restoreKeys {
                +"poetry-master"
            }
//         Локальный путь к директории файла кэша
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
        fileArtifacts {
            repository = FileRepository(name = "mono-rep-artifacts", remoteBasePath = "api")
            localPath = "api/"
            remotePath = "build.gz"
            // Fail job if build/publish/app/ is not found
            optional = false
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
                    api.secrets["DEPLOY_PK"] = Ref("project:PROD__DEPLOY_PK")
                    api.secrets["CACHE_ACCESS_KEY"] = Ref("project:PROD__CACHE_ACCESS_KEY")
                    api.secrets["ARTIFACTS_ACCESS_KEY"] = Ref("project:PROD__ARTIFACTS_ACCESS_KEY")

                    // params
                    api.parameters["SSH_PORT"] = Ref("project:PROD__SSH_PORT")
                    api.parameters["SSH_HOST"] = Ref("project:PROD__SSH_HOST")
                    api.parameters["SSH_USER"] = Ref("project:PROD__SSH_USER")
                }

                "DEV" -> {
                    // secrets
                    api.secrets["DEPLOY_PK"] = Ref("project:DEV__DEPLOY_PK")
                    api.secrets["CACHE_ACCESS_KEY"] = Ref("project:DEV__CACHE_ACCESS_KEY")
                    api.secrets["ARTIFACTS_ACCESS_KEY"] = Ref("project:DEV__ARTIFACTS_ACCESS_KEY")

                    // params
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
        env["ARTIFACTS_PATH"] = "mono-rep-artifacts/api/build.gz"
        env["DESTINATION_PATH"] = "/usr/local/src/flirtex/api"

        shellScript {
            content = """
                    echo ${'$'}DEPLOY_PK | base64 --decode > id_rsa
                    chmod 400 id_rsa
                    ssh-keyscan -p ${'$'}SSH_PORT ${'$'}SSH_HOST >> ./known_hosts
                    scp -i id_rsa \
                        -o UserKnownHostsFile=/dev/null \
                        -o StrictHostKeyChecking=no \
                        -P ${'$'}SSH_PORT \
                        -r ./docker-compose.yml \
                        ${'$'}SSH_USER@${'$'}SSH_HOST:/usr/local/src/flirtex/
                    ssh -i id_rsa \
                        -o UserKnownHostsFile=./known_hosts \
                        -o StrictHostKeyChecking=no \
                        -o LogLevel=INFO \
                        -p ${'$'}SSH_PORT \
                        ${'$'}SSH_USER@${'$'}SSH_HOST "\
                        rm -rf ${'$'}DESTINATION_PATH/*
                        echo Start downloading artifacts on ${'$'}ARTIFACTS_PATH
                        curl -f -L \
                            -H 'Authorization: Bearer ${'$'}ARTIFACTS_ACCESS_KEY' \
                            https://files.pkg.jetbrains.space/flirtex/p/connecta/${'$'}ARTIFACTS_PATH | \
                        tar -xz -C ${'$'}DESTINATION_PATH
                        cd /usr/local/src/flirtex
                        echo Running container
                        docker compose up --build -d api
                        "
              """.trimIndent()
        }
        requirements {
            workerTags("ProdPool-1")
        }
    }
}

job("Web App deploy") {
    startOn {}
    parameters {
        text("ARTIFACTS_PATH", "mono-rep-artifacts/webapp/dist.gz")
        text("DESTINATION_PATH", "/usr/local/src/flirtex/webapp")
        text("ENVIRONMENT", value = "PROD")
    }
    container(displayName = "Building and testing...", image = "node:21-alpine3.18") {
        cache {
            // Генерация имени файла кэша
            // Использование хэша файла pyproject.toml гарантирует, что все запуски задач с
            // одинаковым pyproject.toml будут использовать кэшированные зависимости
            storeKey = "webapp-{{ hashFiles('webapp/package.json') }}"

            // Вариант восстановления
            // Если нужный файл кэша не найден, использовать кэш из 'poetry-master.tar.gz'
            restoreKeys {
                +"webapp-master"
            }

            // Локальный путь к директории файла кэша
            localPath = "webapp/node_modules"
        }

        shellScript {
            content = """
            cd webapp && \
            yarn install && \
            yarn build
            """
        }
        fileArtifacts {
            repository = FileRepository(name = "mono-rep-artifacts", remoteBasePath = "webapp")
            localPath = "webapp/dist/"
            remotePath = "dist.gz"
            // Fail job if build/publish/app/ is not found
            optional = false
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
                    api.secrets["DEPLOY_PK"] = Ref("project:PROD__DEPLOY_PK")
                    api.secrets["CACHE_ACCESS_KEY"] = Ref("project:PROD__CACHE_ACCESS_KEY")
                    api.secrets["ARTIFACTS_ACCESS_KEY"] = Ref("project:PROD__ARTIFACTS_ACCESS_KEY")

                    // params
                    api.parameters["SSH_PORT"] = Ref("project:PROD__SSH_PORT")
                    api.parameters["SSH_HOST"] = Ref("project:PROD__SSH_HOST")
                    api.parameters["SSH_USER"] = Ref("project:PROD__SSH_USER")
                }

                "DEV" -> {
                    // secrets
                    api.secrets["DEPLOY_PK"] = Ref("project:DEV__DEPLOY_PK")
                    api.secrets["CACHE_ACCESS_KEY"] = Ref("project:DEV__CACHE_ACCESS_KEY")
                    api.secrets["ARTIFACTS_ACCESS_KEY"] = Ref("project:DEV__ARTIFACTS_ACCESS_KEY")

                    // params
                    api.parameters["SSH_PORT"] = Ref("project:DEV__SSH_PORT")
                    api.parameters["SSH_HOST"] = Ref("project:DEV__SSH_HOST")
                    api.parameters["SSH_USER"] = Ref("project:DEV__SSH_USER")
                }
            }

        }
    }

    host(displayName = "Deploying...") {

        env["SSH_HOST"] = "{{ SSH_HOST }}"
        env["SSH_PORT"] = "{{ SSH_PORT }}"
        env["SSH_USER"] = "{{ SSH_USER }}"
        env["DEPLOY_PK"] = "{{ DEPLOY_PK }}"
        env["CACHE_ACCESS_KEY"] = "{{ CACHE_ACCESS_KEY }}"
        env["ARTIFACTS_ACCESS_KEY"] = "{{ ARTIFACTS_ACCESS_KEY }}"
        env["ARTIFACTS_PATH"] = "{{ ARTIFACTS_PATH }}"
        env["DESTINATION_PATH"] = "{{ DESTINATION_PATH }}"

        shellScript {
            content = """
                    echo ${'$'}DEPLOY_PK | base64 --decode > id_rsa
                    chmod 400 id_rsa
                    ssh-keyscan -p ${'$'}SSH_PORT ${'$'}SSH_HOST >> ./known_hosts
                    ssh -i id_rsa \
                        -o UserKnownHostsFile=./known_hosts \
                        -o StrictHostKeyChecking=no \
                        -o LogLevel=INFO \
                        -p ${'$'}SSH_PORT \
                        ${'$'}SSH_USER@${'$'}SSH_HOST "\
                        rm -rf ${'$'}DESTINATION_PATH/*
                        echo Start downloading artifacts on ${'$'}ARTIFACTS_PATH
                        curl -f -L \
                            -H 'Authorization: Bearer ${'$'}ARTIFACTS_ACCESS_KEY' \
                            https://files.pkg.jetbrains.space/flirtex/p/connecta/${'$'}ARTIFACTS_PATH | \
                        tar -xz -C ${'$'}DESTINATION_PATH
                        "
              """.trimIndent()
        }
        requirements {
            workerTags("ProdPool-1")
        }
    }
}

job("Run on git push on ./api/") {
    startOn {
        gitPush {
            enabled = true,
            anyBranchMatching {
                +"refs/heads/test"
            }
            pathFilter {
                +"api/**"
            }
        }
    }
    host("Start deployment API to TEST server") {
        env["KEYBASE64"] = "{{ project:KEYBASE64 }}"
        env["SSH_USER"] = "{{ project:TEST_SSH_USER }}"
        env["SSH_PASS"] = "{{ project:TEST_SSH_PASS }}"
        env["SERVER_IP"] = "{{ project:TEST_SERVER_IP }}"

        shellScript {
            content = """
                echo ${'$'}KEYBASE64 | base64 --decode > id_rsa
                chmod 400 id_rsa
                ssh -i id_rsa \
                    -o UserKnownHostsFile=/dev/null \
                    -o StrictHostKeyChecking=no \
                    -o LogLevel=quiet \
                    ${'$'}SSH_USER@${'$'}SERVER_IP "\
                     cd backend/api && \ 
                     git pull origin test &&\
                     docker-compose up -d fastapi_app"
            """
        }
    }
}

job("Run on git push on ./pg-db/") {
    startOn {
        gitPush {
            enabled = false,
            branchFilter {
                +"refs/heads/test"
            }
            pathFilter {
                +"/pg-db"
            }
        }
    }
    host("Start deployment api to PI") {
        env["KEYBASE64"] = "{{ project:KEYBASE64 }}"
        env["SSH_USER"] = "{{ project:TEST_SSH_USER }}"
        env["SSH_PASS"] = "{{ project:TEST_SSH_PASS }}"
        env["SERVER_IP"] = "{{ project:TEST_SERVER_IP }}"

        shellScript {
            content = """
                echo ${'$'}KEYBASE64 | base64 --decode > id_rsa
                chmod 400 id_rsa
                ssh -i id_rsa \
                    -o UserKnownHostsFile=/dev/null \
                    -o StrictHostKeyChecking=no \
                    -o LogLevel=quiet \
                    ${'$'}SSH_USER@${'$'}SERVER_IP "\
                     cd backend/api && \ 
                     git pull origin test &&\
                     docker-compose up -d pg-db"
            """
        }
    }
}

job("Run on git push on ./redis/") {
    startOn {
        gitPush {
            enabled = false,
            branchFilter {
                +"refs/heads/test"
            }
            pathFilter {
                +"./redis/"
            }
        }
    }
    host("Start deployment api to PI") {
        env["KEYBASE64"] = "{{ project:KEYBASE64 }}"
        env["SSH_USER"] = "{{ project:TEST_SSH_USER }}"
        env["SSH_PASS"] = "{{ project:TEST_SSH_PASS }}"
        env["SERVER_IP"] = "{{ project:TEST_SERVER_IP }}"

        shellScript {
            content = """
                echo ${'$'}KEYBASE64 | base64 --decode > id_rsa
                chmod 400 id_rsa
                ssh -i id_rsa \
                    -o UserKnownHostsFile=/dev/null \
                    -o StrictHostKeyChecking=no \
                    -o LogLevel=quiet \
                    ${'$'}SSH_USER@${'$'}SERVER_IP "\
                     cd backend/api && \ 
                     git pull origin test &&\
                     docker-compose up -d redis"
            """
        }
    }
}

job("Run on git push on ./rabbitmq/") {
    startOn {
        gitPush {
            enabled = false,
            branchFilter {
                +"refs/heads/test"
            }
            pathFilter {
                +"./rabbitmq/"
            }
        }
    }
    host("Start deployment api to PI") {
        env["KEYBASE64"] = "{{ project:KEYBASE64 }}"
        env["SSH_USER"] = "{{ project:TEST_SSH_USER }}"
        env["SSH_PASS"] = "{{ project:TEST_SSH_PASS }}"
        env["SERVER_IP"] = "{{ project:TEST_SERVER_IP }}"

        shellScript {
            content = """
                echo ${'$'}KEYBASE64 | base64 --decode > id_rsa
                chmod 400 id_rsa
                ssh -i id_rsa \
                    -o UserKnownHostsFile=/dev/null \
                    -o StrictHostKeyChecking=no \
                    -o LogLevel=quiet \
                    ${'$'}SSH_USER@${'$'}SERVER_IP "\
                     cd backend/api && \ 
                     git pull origin test &&\
                     docker-compose up -d rabbitmq"
            """
        }
    }
}

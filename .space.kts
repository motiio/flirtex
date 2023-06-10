job("Run on git push") {
    startOn {
        gitPush {
            branchFilter {
                +"refs/heads/test"
            }
            pathFilter {
                +"api/"
            }
        }
    }
// for optimisation puporse: do not run any container, put script just on "host": https://www.jetbrains.com/help/space/jobs-and-actions.html#main-features-of-jobs-and-steps
    host("SSH to Test env") {
        env["KEYBASE64"] = "{{ project:KEYBASE64 }}"
        env["HUB_USER"] = "{{ project:JB_DOCKER_LOGIN }}"
        env["HUB_TOKEN"] = "{{ project:JB_DOCKER_PASS }}"
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
                    docker login connecta.registry.jetbrains.space \
                           --username ${'$'}HUB_USER \
                           --password "${'$'}HUB_TOKEN" \
                     && cd api && git pull origin test \
                     && sh deploy_api.sh"
            """
        }
    }
}

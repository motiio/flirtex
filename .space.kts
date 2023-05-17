job("Run on git push") {
    startOn {
        gitPush {
            branchFilter {
                +"refs/heads/test"
            }
        }
    }
    // container(displayName = "Tests...", image = "node:19-alpine") {
    // env["REGISTRY"] = "https://npm.pkg.jetbrains.space/mycompany/p/projectkey/mynpm"
    // shellScript {
//     interpreter = "/bin/bash"
    // content = """
    // echo Install npm dependencies...
    // npm install
    // echo Run build if it exists in package.json...
    // npm run build --if-present
    // echo Run tests...
    // CI=true npm test
    // """
    // }
    // }

    host("Build and push a Docker image...") {
        dockerBuildPush {
            // by default, the step runs not only 'docker build' but also 'docker push'
            // to disable pushing, add the following line:
            // push = false

            // path to Docker context (by default, context is working dir)
//             context = "docker buildx -f docker/Dockerfile.test --platform linux/arm64 && echo"
            // path to Dockerfile relative to the project root
            // if 'file' is not specified, Docker will look for it in 'context'/Dockerfile
            file = "docker/Dockerfile.test"
            // build-time variables
            // image labels
            labels["vendor"] = "connecta"
//            platform = "linux/arm64"
            // to add a raw list of additional build arguments, use
//            extraArgsForBuildCommand = listOf("--platform", "linux/arm64")
            // to add a raw list of additional push arguments, use
            // extraArgsForPushCommand = listOf("...")
            // image tags
            tags {
                // use current job run number as a tag - '0.0.run_number'
                +"connecta.registry.jetbrains.space/p/connecta/containers/api:latest"
            }
        }
    }

    // for optimisation puporse: do not run any container, put script just on "host": https://www.jetbrains.com/help/space/jobs-and-actions.html#main-features-of-jobs-and-steps
    host("SSH to Production") {
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
                ssh -i id_rsa -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -o LogLevel=quiet ${'$'}SSH_USER@${'$'}SERVER_IP "docker login connecta.registry.jetbrains.space --username ${'$'}HUB_USER --password "${'$'}HUB_TOKEN" && sh deploy_api.sh"
            """
        }
    }
}

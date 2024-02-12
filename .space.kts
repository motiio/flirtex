job("[PROD]. API deploy") {
    startOn {}

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

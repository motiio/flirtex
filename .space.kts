job("Example shell scripts") {
    container(image = "ubuntu") {
        shellScript {
            interpreter = "/bin/bash"
            content = """
                echo 'Blya'
            """
        }
    }
}

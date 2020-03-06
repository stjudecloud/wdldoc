task greet {
    String message
    String name

    command {
        echo '${message}, ${name}'
    }

    output {
        String response = read_string(stdout())
    }
}

workflow hello_world {
    String message
    String name

    call greet { input: name=name, message=message }

    parameter_meta {
        message: "Message to greet `name` with."
        name: "Name of the individual to greet."
    }
}
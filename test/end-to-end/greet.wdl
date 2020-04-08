## # Simple task

version 1.0

task greet {
    input {
        String message
        String name
    }

    parameter_meta {
        message: "Message to print"
        name: "Name to address"
    }

    command {
        echo '${message}, ${name}'
    }

    output {
        String response = read_string(stdout())
    }
}

## # Simple workflow

version 1.0

import "greet.wdl"

workflow hello_world {
    input {
        String message
        String name
    }

    call greet.greet { input: name=name, message=message }

    parameter_meta {
        message: "Message to greet `name` with."
        name: "Name of the individual to greet."
    }
}

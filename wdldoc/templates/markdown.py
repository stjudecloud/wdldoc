import re
from typing import Any, DefaultDict, Dict

import WDL as wdl


class MarkDownDoc:
    def __init__(self, title: str) -> None:
        self.title = f"# {title}\n"
        self.front_matter = ""
        self.inputs = "## Inputs\n\n"
        self.outputs = "## Outputs\n\n"
        self.todo = "## To Do\n\n"

    def generate_frontmatter(self, source_text: str) -> None:
        comments = re.findall("^##.*", source_text, re.MULTILINE)
        for comment in comments:
            self.front_matter += comment[3:] + "\n"

    def generate_inputs(
        self,
        inputs: DefaultDict[str, DefaultDict[str, wdl.Env.Binding]],
        parameter_metadata: Dict[str, Any],
    ) -> None:
        if inputs["required"].items():
            self.inputs += "#### Required\n"
        for name, value in inputs["required"].items():
            self.inputs += f"  * `{name}` ({value.type}, **required**)"
            description = parameter_metadata.get(value.name)
            if description:
                self.inputs += ": {}".format(description)
            self.inputs += "\n"

        if inputs["optional"].items():
            self.inputs += "#### Optional\n"
        for name, value in inputs["optional"].items():
            self.inputs += f"  * `{name}` ({value.type})"
            description = parameter_metadata.get(value.name)
            if description:
                self.inputs += ": {}".format(description)
            self.inputs += "\n"

        if inputs["default"].items():
            self.inputs += "#### Defaults\n"
        for name, value in inputs["default"].items():
            self.inputs += f"  * `{name}` ({value.type}, default={value.expr})"
            description = parameter_metadata.get(value.name)
            if description:
                self.inputs += ": {}".format(description)
            self.inputs += "\n"

        if self.inputs == "## Inputs\n\n":
            self.inputs += "None\n"

    def generate_outputs(self, outputs: wdl.Env.Bindings) -> None:
        for output in outputs:
            self.outputs += f"  * `{output.name}` ({output.value})\n"

        if self.outputs == "## Outputs\n\n":
            self.outputs += "None\n"

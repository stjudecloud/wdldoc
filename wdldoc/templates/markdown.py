import re
from typing import Any, DefaultDict, Dict, Union

import WDL as wdl


class MarkDownNode:
    def __init__(self) -> None:
        self.title = ""
        self.header = ""
        self.meta = ""
        self.inputs = "\n### Inputs"
        self.outputs = "\n### Outputs"

    def set_title(self, title: str) -> None:
        self.title = "\n## " + title + "\n"

    def generate_header(self, source_text: str) -> None:
        comments = re.findall("^##.*", source_text, re.MULTILINE)
        for comment in comments:
            self.header += comment[3:] + "\n"

    def generate_meta(self, meta: Dict[str, Any]) -> None:
        for key, value in meta.items():
            self.meta += f"\n{key}\n: {value}\n"

    def _parse_description(
        self, description: Union[str, Any], keys: Dict[str, str]
    ) -> None:
        if isinstance(description, str):
            self.inputs += ": {}".format(description)
            return
        if keys["description"] in description:
            self.inputs += ": {}".format(description[keys["description"]])
            del description[keys["description"]]
            if keys["choices"] in description:
                self.inputs += "; **Choices**: {}".format(description[keys["choices"]])
                del description[keys["choices"]]
        for key in description:
            self.inputs += "; **{}**: {}".format(key, description[key])

    def generate_inputs(
        self,
        inputs: DefaultDict[str, DefaultDict[str, wdl.Env.Binding]],
        parameter_metadata: Dict[str, Any],
        keys: Dict[str, str],
    ) -> None:
        if inputs["required"].items():
            self.inputs += "\n\n#### Required\n"
        for name, value in sorted(
            inputs["required"].items(), key=lambda i: (i[0].count("."), i[0])
        ):
            self.inputs += f"\n  * `{name}` ({value.type}, **required**)"
            description = parameter_metadata.get(value.name)
            if description:
                self._parse_description(description, keys)

        if inputs["optional"].items():
            self.inputs += "\n\n#### Optional\n"
        for name, value in sorted(
            inputs["optional"].items(), key=lambda i: (i[0].count("."), i[0])
        ):
            self.inputs += f"\n  * `{name}` ({value.type})"
            description = parameter_metadata.get(value.name)
            if description:
                self._parse_description(description, keys)

        if inputs["default"].items():
            self.inputs += "\n\n#### Defaults\n"
        for name, value in sorted(
            inputs["default"].items(), key=lambda i: (i[0].count("."), i[0])
        ):
            self.inputs += f"\n  * `{name}` ({value.type}, default={value.expr})"
            description = parameter_metadata.get(value.name)
            if description:
                self._parse_description(description, keys)

        if self.inputs == "\n### Inputs":
            self.inputs += "\n**None**\n"
        else:
            self.inputs += "\n"

    def generate_outputs(self, outputs: wdl.Env.Bindings) -> None:
        self.outputs += "\n"
        for output in outputs:
            self.outputs += f"\n  * `{output.name}` ({output.value})"

        if self.outputs == "\n### Outputs\n":
            self.outputs += "**None**\n"
        else:
            self.outputs += "\n"

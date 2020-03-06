from collections import defaultdict
from typing import DefaultDict

import WDL as wdl
from logzero import logger


def classify_inputs(
    workflow: wdl.Workflow,
) -> DefaultDict[str, DefaultDict[str, wdl.Env.Binding]]:
    results: DefaultDict[str, DefaultDict[str, wdl.Env.Binding]] = defaultdict(
        lambda: defaultdict(dict)
    )

    for b in reversed(list(workflow.available_inputs)):
        assert isinstance(b, wdl.Env.Binding)
        var_name, var_value = str(b.name), b.value
        if not b.value.expr and not b.value.type.optional:
            results["required"][var_name] = var_value
        elif b.value.expr and not b.value.type.optional:
            results["default"][var_name] = var_value
        elif b.value.type.optional:
            results["optional"][var_name] = var_value

    return results

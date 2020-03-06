#!/usr/bin/env python3

import argparse
import sys
from collections import defaultdict
from typing import DefaultDict, Dict

import WDL as wdl


def classify_inputs(
    workflow: wdl.Workflow,
) -> DefaultDict[str, DefaultDict[str, Dict[str, str]]]:
    results: DefaultDict[str, DefaultDict[str, Dict[str, str]]] = defaultdict(
        lambda: defaultdict(dict)
    )

    for b in reversed(list(workflow.available_inputs)):
        assert isinstance(b, wdl.Env.Binding)
        var_name, var_value = str(b.name), dict(b.value)
        if not b.value.expr and not b.value.type.optional:
            results["required"][var_name] = var_value
        elif b.value.expr and not b.value.type.optional:
            results["default"][var_name] = var_value
        elif b.value.type.optional:
            results["optional"][var_name] = var_value

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate clean WDL documentation from source."
    )
    parser.add_argument("file", help="Either a WDL tool or a WDL workflow.", type=str)
    parser.add_argument(
        "-o", "--output", help="File to direct output to.", type=str, default=sys.stdout
    )
    args = parser.parse_args()

    _handle = args.output
    if args.output is not sys.stdout:
        _handle = open(_handle, "w")

    document = wdl.load(args.file)
    if not getattr(document, "workflow"):
        raise RuntimeError("Currently, only workflows are supported.")

    workflow = document.workflow
    print(workflow.parameter_meta, file=sys.stderr)
    print(document.tasks, file=sys.stderr)
    inputs = classify_inputs(workflow)

    print("# Workflow", file=_handle)
    print("", file=_handle)
    print("## Inputs", file=_handle)
    print("", file=_handle)
    for name, value in inputs["required"].items():
        print(
            f"  * {value.get('name')} ({value.get('type')}, **required**):",
            file=_handle,
        )

    _handle.close()

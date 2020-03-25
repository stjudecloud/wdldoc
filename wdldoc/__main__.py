#!/usr/bin/env python3

import argparse
import logging
import sys

import WDL as wdl

import logzero

from . import classify_inputs
from .miniwdl.sources import read_source


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate clean WDL documentation from source."
    )
    parser.add_argument("file", help="Either a WDL tool or a WDL workflow.", type=str)
    parser.add_argument(
        "-o", "--output", help="File to direct output to.", type=str, default=sys.stdout
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Sets the log level to INFO.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--debug",
        help="Sets the log level to DEBUG.",
        default=False,
        action="store_true",
    )
    args = parser.parse_args()

    logzero.loglevel(logging.WARNING)
    if args.verbose:
        logzero.loglevel(logging.INFO)
    if args.debug:
        logzero.loglevel(logging.DEBUG)

    _handle = args.output
    if args.output is not sys.stdout:
        _handle = open(_handle, "w")

    document = wdl.load(args.file, read_source=read_source)
    if not getattr(document, "workflow"):
        raise RuntimeError("Currently, only workflows are supported.")

    workflow = document.workflow
    parameter_metadata = workflow.parameter_meta
    inputs = classify_inputs(workflow)

    print("# Workflow", file=_handle)
    print("", file=_handle)
    print("## Inputs", file=_handle)
    print("", file=_handle)
    for name, value in inputs["required"].items():
        message = f"  * `{name}` ({value.type}, **required**)"
        description = parameter_metadata.get(value.name)
        if description:
            message += ": {}".format(description)
        print(message, file=_handle)
    for name, value in inputs["optional"].items():
        message = f"  * `{name}` ({value.type})"
        description = parameter_metadata.get(value.name)
        if description:
            message += ": {}".format(description)
        print(message, file=_handle)
    for name, value in inputs["default"].items():
        message = f"  * `{name}` ({value.type}, default={value.expr})"
        description = parameter_metadata.get(value.name)
        if description:
            message += ": {}".format(description)
        print(message, file=_handle)

    _handle.close()

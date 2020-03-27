#!/usr/bin/env python3

import argparse
import logging
import sys

import WDL as wdl

import logzero

from . import classify_inputs
from .miniwdl.sources import read_source
from .templates.markdown import MarkDownDoc


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

    try:
        document = wdl.load(args.file, read_source=read_source)
    except wdl.Error.SyntaxError as e:
        logzero.logger.error(f"{e.__class__.__name__}: {e}")
        sys.exit(1)
    except wdl.Error.ValidationError as e:
        logzero.logger.error(f"{e.__class__.__name__}: {e}")
        sys.exit(1)
    except wdl.Error.RuntimeError as e:
        logzero.logger.error(f"{e.__class__.__name__}: {e}")
        sys.exit(1)
    except wdl.Error.ImportError as e:
        logzero.logger.error(f"{e.__class__.__name__}: {e}")
        sys.exit(1)
    except wdl.Error.MultipleValidationErrors as e:
        logzero.logger.error(f"{e.__class__.__name__}: {e}")
        sys.exit(1)

    if not getattr(document, "workflow"):
        raise RuntimeError("Currently, only workflows are supported.")

    workflow = document.workflow
    parameter_metadata = workflow.parameter_meta
    inputs = classify_inputs(workflow)

    doc = MarkDownDoc()
    doc.generate_frontmatter(document.source_text)
    doc.generate_inputs(inputs, parameter_metadata)
    doc.generate_outputs(workflow.effective_outputs)
    print(doc.front_matter, file=_handle)
    print(doc.inputs, file=_handle)
    print(doc.outputs, file=_handle)

    _handle.close()

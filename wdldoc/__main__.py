#!/usr/bin/env python3

import argparse
import logging
import sys

import logzero

from .bin.wdldoc import single_file, traverse_directory


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate clean WDL documentation from source."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "directory",
        nargs="?",
        help="Top level directory to search for WDL files.",
        type=str,
    )
    group.add_argument("-f", "--file", help="A WDL workflow file.", type=str)
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

    if args.file:
        output = args.output
        if args.output is not sys.stdout:
            output = open(args.output, "w")
        single_file(args.file, output)
    else:
        traverse_directory(args.directory)

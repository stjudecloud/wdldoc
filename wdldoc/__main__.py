#!/usr/bin/env python3

import argparse
import logging
import os

import logzero

from .bin.wdldoc import parse_file, traverse_directory


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate clean WDL documentation from source."
    )
    parser.add_argument(
        "sources",
        nargs="+",
        help="Top level directories to search for WDL files, "
        "or the WDL files themselves.",
        type=str,
    )
    parser.add_argument(
        "-o",
        "--output_directory",
        help="Directory to store markdown files.",
        default="./documentation",
        type=str,
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

    for source in args.sources:
        if os.path.isdir(source):
            traverse_directory(source, args.output_directory)
        elif os.path.isfile(source):
            parse_file(source, args.output_directory)
        else:
            raise RuntimeError(f"Could not find {source}.")

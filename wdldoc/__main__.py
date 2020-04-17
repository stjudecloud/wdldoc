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
        help="Directory to store markdown files. Default is `./documentation`",
        default="./documentation",
        type=str,
    )
    parser.add_argument(
        "-d",
        "--description",
        help="If parameter meta fields use a JSON object, the key "
        "for the field containing the input description. "
        "Default is 'help'. Ignored if only strings are used.",
        default="help",
        type=str,
    )
    parser.add_argument(
        "-c",
        "--choices",
        help="If parameter meta fields use a JSON object, the key "
        "for the field containing the input choices. "
        "Default is 'choices'. Ignored if only strings are used.",
        default="choices",
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

    keys = {"description": args.description, "choices": args.choices}

    for source in args.sources:
        if os.path.isdir(source):
            traverse_directory(source, args.output_directory, keys)
        elif os.path.isfile(source):
            parse_file(source, args.output_directory, keys)
        else:
            raise RuntimeError(f"Could not find {source}.")

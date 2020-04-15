import glob
import os
import pathlib
import sys
from typing import TextIO, Union

import WDL as wdl

import logzero

from .. import classify_inputs
from ..miniwdl.sources import read_source
from ..templates.markdown import MarkDownNode


def document_node(node: Union[wdl.Workflow, wdl.Task], doc: MarkDownNode) -> None:
    doc.set_title(node.name)
    parameter_metadata = node.parameter_meta
    inputs = classify_inputs(node)
    doc.generate_inputs(inputs, parameter_metadata)
    doc.generate_outputs(node.effective_outputs)
    doc.generate_meta(node.meta)


def document_workflow(document: wdl.Document, output: TextIO) -> None:
    doc = MarkDownNode()
    doc.generate_frontmatter(document.source_text)
    document_node(document.workflow, doc)
    print(doc.front_matter, end="", file=output)
    print(doc.title, end="", file=output)
    print(doc.meta, end="", file=output)
    print(doc.inputs, end="", file=output)
    print(doc.outputs, end="", file=output)


def document_task(task: wdl.Task, output: TextIO) -> None:
    doc = MarkDownNode()
    document_node(task, doc)
    print(doc.title, end="", file=output)
    print(doc.meta, end="", file=output)
    print(doc.inputs, end="", file=output)
    print(doc.outputs, end="", file=output)


def parse_file(file: str, outdir: str, fast_fail: bool = False) -> None:
    failure = False
    try:
        document = wdl.load(file, read_source=read_source)
    except FileNotFoundError as e:
        logzero.logger.error(f"{e.__class__.__name__}: {e}")
        failure = True
    except wdl.Error.SyntaxError as e:
        logzero.logger.error(f"{e.__class__.__name__}: {e}")
        failure = True
    except wdl.Error.ValidationError as e:
        logzero.logger.error(f"{e.__class__.__name__}: {e}")
        failure = True
    except wdl.Error.RuntimeError as e:
        logzero.logger.error(f"{e.__class__.__name__}: {e}")
        failure = True
    except wdl.Error.ImportError as e:
        logzero.logger.error(f"{e.__class__.__name__}: {e}")
        failure = True
    except wdl.Error.MultipleValidationErrors as e:
        logzero.logger.error(f"{e.__class__.__name__}: {e}")
        failure = True

    if fast_fail and failure:
        sys.exit(1)
    elif failure:
        logzero.logger.error(f"Skipping {file}")
        return

    logzero.logger.info(f"Generating docs for {file}")

    outfile_basename = "".join(os.path.basename(file).split(".")[:-1]) + ".md"

    if getattr(document, "workflow"):
        new_filename = os.path.join(outdir, "workflows", outfile_basename)
        pathlib.Path(os.path.dirname(new_filename)).mkdir(parents=True, exist_ok=True)
        output = open(new_filename, "w")
        document_workflow(document, output)
        for task in document.tasks:
            document_task(task, output)
        output.close()
    elif getattr(document, "tasks"):
        new_filename = os.path.join(outdir, "tasks", outfile_basename)
        pathlib.Path(os.path.dirname(new_filename)).mkdir(parents=True, exist_ok=True)
        output = open(new_filename, "w")
        doc = MarkDownNode()
        doc.generate_frontmatter(document.source_text)
        print(doc.front_matter, end="", file=output)
        for task in document.tasks:
            document_task(task, output)
        output.close()
    else:
        logzero.logger.warning(f"{file} has no task or workflow definitions.")


def traverse_directory(dir: str, outdir: str) -> None:
    files = glob.glob(dir + f"{os.path.sep}**{os.path.sep}*.wdl", recursive=True)
    for file in files:
        parse_file(file, outdir)

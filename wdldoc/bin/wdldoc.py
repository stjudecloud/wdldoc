import glob
import os
import pathlib
import sys
from typing import TextIO

import WDL as wdl

import logzero

from .. import classify_inputs
from ..miniwdl.sources import read_source
from ..templates.markdown import MarkDownDoc


def single_file(file: str, output: TextIO, fast_fail: bool = False) -> None:

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
        logzero.logger.info(f"Skipping {file}")
        return

    if not getattr(document, "workflow"):
        if fast_fail:
            raise RuntimeError("Currently, only workflows are supported.")
        logzero.logger.info(f"Skipping {file} because it's not a workflow.")
        return

    logzero.logger.info(f"Generating docs for {file}")

    workflow = document.workflow
    parameter_metadata = workflow.parameter_meta
    inputs = classify_inputs(workflow)

    doc = MarkDownDoc()
    doc.generate_frontmatter(document.source_text)
    doc.generate_inputs(inputs, parameter_metadata)
    doc.generate_outputs(workflow.effective_outputs)
    print(doc.front_matter, file=output)
    print(doc.inputs, file=output)
    print(doc.outputs, file=output)

    output.close()


def traverse_directory(dir: str) -> None:
    docs_dir = os.path.join(dir, "documentation")
    # pathlib.Path(docs_dir).mkdir(exist_ok=True)
    files = glob.glob(dir + f"{os.path.sep}**{os.path.sep}*.wdl", recursive=True)
    for file in files:
        source_dir = os.path.dirname(file)
        outfile_basename = "".join(os.path.basename(file).split(".")[:-1]) + ".md"
        new_file = os.path.join(docs_dir, source_dir.replace(dir, ""), outfile_basename)
        pathlib.Path(os.path.dirname(new_file)).mkdir(parents=True, exist_ok=True)
        output = open(new_file, "w")
        single_file(file, output)

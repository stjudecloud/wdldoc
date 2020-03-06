import os
import tempfile
import urllib

import WDL as wdl
from logzero import logger


async def read_source(uri, path, importer):
    logger.debug(f"Reading source: {uri}")
    if uri.startswith("http:") or uri.startswith("https:"):
        fn = os.path.join(
            tempfile.mkdtemp(prefix="wdldoc_"),
            os.path.basename(urllib.parse.urlsplit(uri).path),
        )
        urllib.request.urlretrieve(uri, filename=fn)
        with open(fn, "r") as infile:
            return wdl.ReadSourceResult(infile.read(), uri)
    elif importer and (
        importer.pos.abspath.startswith("http:")
        or importer.pos.abspath.startswith("https:")
    ):
        assert not os.path.isabs(uri), "absolute import from downloaded WDL"
        return await read_source(
            urllib.parse.urljoin(importer.pos.abspath, uri), [], importer
        )
    return await wdl.read_source_default(uri, path, importer)

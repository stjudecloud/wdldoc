import os
import tempfile
from typing import Optional
from urllib.parse import urljoin, urlsplit
from urllib.request import urlretrieve

import WDL as wdl
from logzero import logger


async def read_source(
    uri: str, path: str, importer: Optional[wdl.Document]
) -> wdl.ReadSourceResult:
    logger.debug(f"Reading source: {uri}")
    if uri.startswith("http:") or uri.startswith("https:"):
        fn = os.path.join(
            tempfile.mkdtemp(prefix="wdldoc_"), os.path.basename(urlsplit(uri).path),
        )
        urlretrieve(uri, filename=fn)
        with open(fn, "r") as infile:
            return wdl.ReadSourceResult(infile.read(), uri)
    elif importer and (
        importer.pos.abspath.startswith("http:")
        or importer.pos.abspath.startswith("https:")
    ):
        assert not os.path.isabs(uri), "absolute import from downloaded WDL"
        return await read_source(urljoin(importer.pos.abspath, uri), "", importer)
    return await wdl.read_source_default(uri, path, importer)

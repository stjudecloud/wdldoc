import os
import tempfile
from typing import Optional
from urllib.parse import urljoin, urlsplit
from urllib.request import urlretrieve

import requests
import WDL as wdl
from logzero import logger

from cachecontrol import CacheControl
from cachecontrol.caches import FileCache

# though `forever` is set, this is still invalidated
# if the ETag does not match (meaning the file underneath)
# changed.
sess = CacheControl(
    requests.Session(),
    cache=FileCache(
        os.path.join(os.path.expanduser("~"), ".wdldoc-cache"), forever=True
    ),
)


async def read_source(
    uri: str, path: str, importer: Optional[wdl.Document]
) -> wdl.ReadSourceResult:
    logger.debug(f"Reading source: {uri}")

    if uri.startswith("http:") or uri.startswith("https:"):
        return wdl.ReadSourceResult(sess.get(uri).text, uri)

    return await wdl.read_source_default(uri, path, importer)

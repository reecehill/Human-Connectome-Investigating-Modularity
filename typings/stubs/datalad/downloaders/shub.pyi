"""
This type stub file was generated by pyright.
"""

from datalad.dochelpers import borrowkwargs
from datalad.downloaders.http import HTTPDownloader
from datalad.utils import auto_repr

"""Support for resolving Singularity Hub URLs
"""
lgr = ...
@auto_repr
class SHubDownloader(HTTPDownloader):
    """Resolve shub:// URLs before handing them off to HTTPDownloader.
    """
    api_url = ...
    @borrowkwargs(HTTPDownloader)
    def __init__(self, *args, **kwargs) -> None:
        ...
    
    @borrowkwargs(HTTPDownloader)
    def access(self, method, url, *args, **kwargs):
        ...
    


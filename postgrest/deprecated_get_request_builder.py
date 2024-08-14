from __future__ import annotations

from deprecation import deprecated

from ._async.request_builder import AsyncSelectRequestBuilder
from .version import __version__


class GetRequestBuilder(AsyncSelectRequestBuilder):
    """Alias to SelectRequestBuilder."""

    @deprecated("0.4.0", "1.0.0", __version__, "Use SelectRequestBuilder instead")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

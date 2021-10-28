from deprecation import deprecated

from postgrest_py.__version__ import __version__
from postgrest_py._async.request_builder import AsyncSelectRequestBuilder


class GetRequestBuilder(AsyncSelectRequestBuilder):
    """Alias to AsyncSelectRequestBuilder."""

    @deprecated("0.4.0", "1.0.0", __version__, "Use AsyncSelectRequestBuilder instead")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

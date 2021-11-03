from deprecation import deprecated

from postgrest_py.__version__ import __version__
from postgrest_py._async.client import AsyncPostgrestClient


class Client(AsyncPostgrestClient):
    """Alias to PostgrestClient."""

    @deprecated("0.2.0", "1.0.0", __version__, "Use PostgrestClient instead")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


PostgrestClient = Client

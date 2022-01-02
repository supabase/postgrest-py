from typing import Dict, cast

from deprecation import deprecated
from httpx import Response

from postgrest_py.__version__ import __version__
from postgrest_py.base_client import (
    DEFAULT_POSTGREST_CLIENT_HEADERS,
    BasePostgrestClient,
)
from postgrest_py.utils import SyncClient

from .request_builder import SyncRequestBuilder


class SyncPostgrestClient(BasePostgrestClient):
    """PostgREST client."""

    def __init__(
        self,
        base_url: str,
        *,
        schema: str = "public",
        headers: Dict[str, str] = DEFAULT_POSTGREST_CLIENT_HEADERS,
    ) -> None:
        BasePostgrestClient.__init__(self, base_url, schema=schema, headers=headers)
        self.session = cast(SyncClient, self.session)

    def create_session(
        self,
        base_url: str,
        headers: Dict[str, str],
    ) -> SyncClient:
        return SyncClient(base_url=base_url, headers=headers)

    def __enter__(self) -> "SyncPostgrestClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.aclose()

    def aclose(self) -> None:
        self.session.aclose()

    def from_(self, table: str) -> SyncRequestBuilder:
        """Perform a table operation."""
        base_url = str(self.session.base_url)
        headers = dict(self.session.headers.items())
        session = self.create_session(base_url, headers)
        session.auth = self.session.auth
        return SyncRequestBuilder(session, f"/{table}")

    def table(self, table: str) -> SyncRequestBuilder:
        """Alias to self.from_()."""
        return self.from_(table)

    @deprecated("0.2.0", "1.0.0", __version__, "Use self.from_() instead")
    def from_table(self, table: str) -> SyncRequestBuilder:
        """Alias to self.from_()."""
        return self.from_(table)

    def rpc(self, func: str, params: dict) -> Response:
        """Perform a stored procedure call."""
        path = f"/rpc/{func}"
        return self.session.post(path, json=params)

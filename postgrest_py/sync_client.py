from __future__  import annotations
from types import TracebackType
from typing import Dict, Optional, Type

from httpx import Client, Response

from postgrest_py.__version__ import __version__
from postgrest_py.base_client import BaseClient
from postgrest_py.constants import DEFAULT_POSTGREST_CLIENT_HEADERS


class PostgrestClient(BaseClient):
    """Synchronous PostgREST client."""

    def __init__(
        self,
        base_url: str,
        *,
        schema: str = "public",
        headers: Dict[str, str] = DEFAULT_POSTGREST_CLIENT_HEADERS,
    ) -> None:
        headers = {
            **headers,
            "Accept-Profile": schema,
            "Content-Profile": schema,
        }
        self.session: Client = Client(base_url=base_url, headers=headers)

    def __enter__(self) -> PostgrestClient:
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], tb: Optional[TracebackType]) -> None:
        self.session.close()

    def close(self) -> None:
        """Close the underlying HTTP transport and proxies."""
        self.session.close()

    def rpc(self, func: str, params: dict) -> Response:
        """Perform a stored procedure call."""
        path = f"/rpc/{func}"
        r = self.session.post(path, json=params)
        return r

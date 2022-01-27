from __future__ import annotations

from typing import Dict, Union, cast

from deprecation import deprecated
from httpx import Response, Timeout

from .. import __version__
from ..base_client import (
    DEFAULT_POSTGREST_CLIENT_HEADERS,
    DEFAULT_POSTGREST_CLIENT_TIMEOUT,
    BasePostgrestClient,
)
from ..utils import AsyncClient
from .request_builder import AsyncRequestBuilder


class AsyncPostgrestClient(BasePostgrestClient):
    """PostgREST client."""

    def __init__(
        self,
        base_url: str,
        *,
        schema: str = "public",
        headers: Dict[str, str] = DEFAULT_POSTGREST_CLIENT_HEADERS,
        timeout: Union[int, float, Timeout] = DEFAULT_POSTGREST_CLIENT_TIMEOUT,
    ) -> None:
        BasePostgrestClient.__init__(
            self,
            base_url,
            schema=schema,
            headers=headers,
            timeout=timeout,
        )
        self.session = cast(AsyncClient, self.session)

    def create_session(
        self,
        base_url: str,
        headers: Dict[str, str],
        timeout: Union[int, float, Timeout],
    ) -> AsyncClient:
        return AsyncClient(
            base_url=base_url,
            headers=headers,
            timeout=timeout,
        )

    async def __aenter__(self) -> AsyncPostgrestClient:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self.session.aclose()

    def from_(self, table: str) -> AsyncRequestBuilder:
        """Perform a table operation."""
        base_url = str(self.session.base_url)
        headers = dict(self.session.headers.items())
        session = self.create_session(base_url, headers, self.session.timeout)
        session.auth = self.session.auth
        return AsyncRequestBuilder(session, f"/{table}")

    def table(self, table: str) -> AsyncRequestBuilder:
        """Alias to self.from_()."""
        return self.from_(table)

    @deprecated("0.2.0", "1.0.0", __version__, "Use self.from_() instead")
    def from_table(self, table: str) -> AsyncRequestBuilder:
        """Alias to self.from_()."""
        return self.from_(table)

    async def rpc(self, func: str, params: dict) -> Response:
        """Perform a stored procedure call."""
        path = f"/rpc/{func}"
        return await self.session.post(path, json=params)

from __future__ import annotations
from typing import Dict, Optional, Type
from types import TracebackType

from deprecation import deprecated
from httpx import AsyncClient, Response

from postgrest_py.__version__ import __version__
from postgrest_py.base_client import BaseClient
from postgrest_py.constants import DEFAULT_POSTGREST_CLIENT_HEADERS


class AsyncPostgrestClient(BaseClient):
    """Asyncio compatible PostgREST client."""

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
        self.session: AsyncClient = AsyncClient(base_url=base_url, headers=headers)

    async def __aenter__(self) -> AsyncPostgrestClient:
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], tb: Optional[TracebackType]) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self.session.aclose()

    async def rpc(self, func: str, params: dict) -> Response:
        """Perform a stored procedure call."""
        path = f"/rpc/{func}"
        r = await self.session.post(path, json=params)
        return r


class Client(AsyncPostgrestClient):
    """Alias to AsyncPostgrestClient."""

    @deprecated("0.2.0", "1.0.0", __version__, "Use AsyncPostgrestClient instead")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

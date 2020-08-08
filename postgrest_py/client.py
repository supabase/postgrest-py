from deprecation import deprecated
from httpx import AsyncClient, Response

from postgrest_py.__version__ import __version__
from postgrest_py.request_builder import RequestBuilder


class PostgrestClient:
    def __init__(self, base_url: str, *, schema="public") -> None:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Accept-Profile": schema,
            "Content-Profile": schema,
        }
        self.session = AsyncClient(base_url=base_url, params={}, headers=headers)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self.session.aclose()

    def auth(self, bearer_token: str, *, username: str = None, password: str = None):
        """Authenticate the request, with either bearer token or basic authentication."""

        if username:
            self.session.auth = (username, password)
        else:
            self.session.headers["Authorization"] = f"Bearer {bearer_token}"
        return self

    def schema(self, schema: str):
        self.session.merge_headers(
            {"Accept-Profile": schema, "Content-Profile": schema}
        )
        return self

    def from_(self, table: str) -> RequestBuilder:
        return RequestBuilder(self.session, f"/{table}")

    @deprecated("0.2.0", "1.0.0", __version__, "Use PostgrestClient.from_() instead")
    def from_table(self, table: str) -> RequestBuilder:
        """Alias to Self.from_()."""

        return self.from_(table)

    async def rpc(self, func: str, params: dict) -> Response:
        """Execute a stored procedure call."""

        path = f"/rpc/{func}"
        r = await self.session.post(path, json=params)
        return r


class Client(PostgrestClient):
    @deprecated("0.2.0", "1.0.0", __version__, "Use PostgrestClient instead")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

from httpx import AsyncClient

from postgrest_py.request_builder import RequestBuilder


class Client:
    def __init__(self, base_url: str, *, schema="public") -> None:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Accept-Profile": schema,
            "Content-Profile": schema,
        }
        self.session = AsyncClient(base_url=base_url, headers=headers)

    async def __aenter__(self) -> Client:
        return self

    async def __aexit__(self) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self.session.aclose()

    def auth(self, token: str) -> Client:
        self.session.headers["Authorization"] = f"Bearer {token}"
        return self

    def schema(self, schema: str) -> Client:
        self.session.merge_headers(
            {"Accept-Profile": schema, "Content-Profile": schema}
        )
        return self

    def fromTable(self, table: str) -> RequestBuilder:
        return RequestBuilder(self.session, table)

from __future__ import annotations

from typing import AnyStr, Optional, TypeVar, Union

from deprecation import deprecated
from httpx import Client, AsyncClient, BasicAuth

from postgrest_py.__version__ import __version__
from postgrest_py.request_builder import RequestBuilder


T = TypeVar("T", bound="BaseClient")


class BaseClient:
    def __init__(self) -> None:
        self.session: Union[Client, AsyncClient]

    def auth(
        self: T,
        token: Optional[str] = None,
        *,
        username: Optional[AnyStr] = None,
        password: AnyStr = "",
    ) -> T:
        """
        Authenticate the client with either bearer token or basic authentication.

        Raise `ValueError` if neither authentication scheme is provided.
        Bearer token is preferred if both ones are provided.
        """
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
        elif username:
            self.session.auth = BasicAuth(username, password)
        else:
            raise ValueError(
                "Neither bearer token or basic authentication scheme is provided"
            )
        return self

    def schema(self: T, schema: str) -> T:
        """Switch to another schema."""
        self.session.headers.update({"Accept-Profile": schema, "Content-Profile": schema})
        return self

    def from_(self, table: str) -> RequestBuilder:
        """Perform a table operation."""
        return RequestBuilder(self.session, f"/{table}")

    @deprecated("0.2.0", "1.0.0", __version__, "Use PostgrestClient.from_() instead")
    def from_table(self, table: str) -> RequestBuilder:
        """Alias to Self.from_()."""
        return self.from_(table)

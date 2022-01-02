from abc import ABC, abstractmethod
from typing import Dict, Optional, Union

from httpx import BasicAuth

from postgrest_py.utils import AsyncClient, SyncClient

DEFAULT_POSTGREST_CLIENT_HEADERS: Dict[str, str] = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class BasePostgrestClient(ABC):
    """Base PostgREST client."""

    def __init__(self, base_url: str, *, schema: str, headers: Dict[str, str]) -> None:
        headers = {
            **headers,
            "Accept-Profile": schema,
            "Content-Profile": schema,
        }
        self.session = self.create_session(base_url, headers)

    @abstractmethod
    def create_session(
        self,
        base_url: str,
        headers: Dict[str, str],
    ) -> Union[SyncClient, AsyncClient]:
        raise NotImplementedError()

    def auth(
        self,
        token: Optional[str],
        *,
        username: Union[str, bytes, None] = None,
        password: Union[str, bytes] = "",
    ):
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

    def schema(self, schema: str):
        """Switch to another schema."""
        self.session.headers.update({"Accept-Profile": schema, "Content-Profile": schema})
        return self

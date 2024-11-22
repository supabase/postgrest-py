from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Optional, Union

from httpx import BasicAuth, Timeout

from .utils import AsyncClient, SyncClient, is_http_url, is_valid_jwt


class BasePostgrestClient(ABC):
    """Base PostgREST client."""

    def __init__(
        self,
        base_url: str,
        *,
        schema: str,
        headers: Dict[str, str],
        timeout: Union[int, float, Timeout],
        verify: bool = True,
        proxy: Optional[str] = None,
    ) -> None:
        if not is_http_url(base_url):
            ValueError("base_url must be a valid HTTP URL string")
        headers = {
            **headers,
            "Accept-Profile": schema,
            "Content-Profile": schema,
        }
        self.session = self.create_session(base_url, headers, timeout, verify, proxy)

    @abstractmethod
    def create_session(
        self,
        base_url: str,
        headers: Dict[str, str],
        timeout: Union[int, float, Timeout],
        verify: bool = True,
        proxy: Optional[str] = None,
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

        Raises:
            `ValueError`: If neither authentication scheme is provided.

        .. note::
            Bearer token is preferred if both ones are provided.
        """
        if token:
            if not is_valid_jwt(token):
                ValueError("token must be a valid JWT authorization token")
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
        self.session.headers.update(
            {
                "Accept-Profile": schema,
                "Content-Profile": schema,
            }
        )
        return self

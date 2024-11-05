from __future__ import annotations

import re
from typing import Any, Type, TypeVar, cast, get_origin
from urllib.parse import urlparse

from httpx import AsyncClient  # noqa: F401
from httpx import Client as BaseClient  # noqa: F401

BASE64URL_REGEX = r"^([a-z0-9_-]{4})*($|[a-z0-9_-]{3}$|[a-z0-9_-]{2}$)$"


class SyncClient(BaseClient):
    def aclose(self) -> None:
        self.close()


def sanitize_param(param: Any) -> str:
    param_str = str(param)
    reserved_chars = ",:()"
    if any(char in param_str for char in reserved_chars):
        return f'"{param_str}"'
    return param_str


def sanitize_pattern_param(pattern: str) -> str:
    return sanitize_param(pattern.replace("%", "*"))


_T = TypeVar("_T")


def get_origin_and_cast(typ: type[type[_T]]) -> type[_T]:
    # Base[T] is an instance of typing._GenericAlias, so doing Base[T].__init__
    # tries to call _GenericAlias.__init__ - which is the wrong method
    # get_origin(Base[T]) returns Base
    # This function casts Base back to Base[T] to maintain type-safety
    # while still allowing us to access the methods of `Base` at runtime
    # See: definitions of request builders that use multiple-inheritance
    # like AsyncFilterRequestBuilder
    return cast(Type[_T], get_origin(typ))


def is_http_url(url: str) -> bool:
    return urlparse(url).scheme in {"https", "http"}


def is_valid_jwt(value: str) -> bool:
    """Checks if value looks like a JWT, does not do any extra parsing."""
    if not isinstance(value, str):
        return False

    # Remove trailing whitespaces if any.
    value = value.strip()

    # Remove "Bearer " prefix if any.
    if value.startswith("Bearer "):
        value = value[7:]

    # Valid JWT must have 2 dots (Header.Paylod.Signature)
    if value.count(".") != 2:
        return False

    for part in value.split("."):
        if not re.search(BASE64URL_REGEX, part, re.IGNORECASE):
            return False

    return True

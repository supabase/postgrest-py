from httpx import AsyncClient  # noqa: F401
from httpx import Client as BaseClient  # noqa: F401


class SyncClient(BaseClient):
    def aclose(self) -> None:
        self.close()


def sanitize_param(param: str) -> str:
    reserved_chars = ",.:()"
    if any(char in param for char in reserved_chars):
        return f"%22{param}%22"
    return param


def sanitize_pattern_param(pattern: str) -> str:
    return sanitize_param(pattern.replace("%", "*"))

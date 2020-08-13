from typing import Iterable, Tuple

from httpx import AsyncClient, Response

from postgrest_py.utils import sanitize_param, sanitize_pattern_param


class RequestBuilder:
    def __init__(self, session: AsyncClient, path: str) -> None:
        self.session = session
        self.path = path
        self.json = {}
        self.http_method = "GET"

        self.negate_next = False

    @property
    def not_(self):
        self.negate_next = True
        return self

    def select(self, *columns: str):
        self.session.params["select"] = ",".join(columns)
        self.http_method = "GET"
        return GetRequestBuilder.from_request_builder(self)

    def insert(self, json: dict, *, upsert=False):
        self.session.headers[
            "Prefer"
        ] = f"return=representation{',resolution=merge-duplicates' if upsert else ''}"
        self.json = json
        self.http_method = "POST"
        return self

    def update(self, json: dict):
        self.session.headers["Prefer"] = "return=representation"
        self.json = json
        self.http_method = "PATCH"
        return self

    def delete(self):
        self.http_method = "DELETE"
        return self

    async def execute(self) -> Response:
        r = await self.session.request(self.http_method, self.path, json=self.json)
        return r

    def filter(self, column: str, operator: str, criteria: str):
        """Either filter in or filter out based on Self.negate_next."""
        if self.negate_next == True:
            self.negate_next = False
            operator = f"not.{operator}"
        self.session.params[sanitize_param(column)] = f"{operator}.{criteria}"
        return self

    def eq(self, column: str, value: str):
        return self.filter(column, "eq", sanitize_param(value))

    def neq(self, column: str, value: str):
        return self.filter(column, "neq", sanitize_param(value))

    def gt(self, column: str, value: str):
        return self.filter(column, "gt", sanitize_param(value))

    def gte(self, column: str, value: str):
        return self.filter(column, "gte", sanitize_param(value))

    def lt(self, column: str, value: str):
        return self.filter(column, "lt", sanitize_param(value))

    def lte(self, column: str, value: str):
        return self.filter(column, "lte", sanitize_param(value))

    def is_(self, column: str, value: str):
        return self.filter(column, "is", sanitize_param(value))

    def like(self, column: str, pattern: str):
        return self.filter(column, "like", sanitize_pattern_param(pattern))

    def ilike(self, column: str, pattern: str):
        return self.filter(column, "ilike", sanitize_pattern_param(pattern))

    def fts(self, column: str, query: str):
        return self.filter(column, "fts", sanitize_param(query))

    def plfts(self, column: str, query: str):
        return self.filter(column, "plfts", sanitize_param(query))

    def phfts(self, column: str, query: str):
        return self.filter(column, "phfts", sanitize_param(query))

    def wfts(self, column: str, query: str):
        return self.filter(column, "wfts", sanitize_param(query))

    def in_(self, column: str, values: Iterable[str]):
        values = map(sanitize_param, values)
        values = ",".join(values)
        return self.filter(column, "in", f"({values})")

    def cs(self, column: str, values: Iterable[str]):
        values = map(sanitize_param, values)
        values = ",".join(values)
        return self.filter(column, "cs", f"{{values}}")

    def cd(self, column: str, values: Iterable[str]):
        values = map(sanitize_param, values)
        values = ",".join(values)
        return self.filter(column, "cd", f"{{values}}")

    def ov(self, column: str, values: Iterable[str]):
        values = map(sanitize_param, values)
        values = ",".join(values)
        return self.filter(column, "ov", f"{{values}}")

    def sl(self, column: str, range: Tuple[int, int]):
        return self.filter(column, "sl", f"({range[0]},{range[1]})")

    def sr(self, column: str, range: Tuple[int, int]):
        return self.filter(column, "sr", f"({range[0]},{range[1]})")

    def nxl(self, column: str, range: Tuple[int, int]):
        return self.filter(column, "nxl", f"({range[0]},{range[1]})")

    def nxr(self, column: str, range: Tuple[int, int]):
        return self.filter(column, "nxr", f"({range[0]},{range[1]})")

    def adj(self, column: str, range: Tuple[int, int]):
        return self.filter(column, "adj", f"({range[0]},{range[1]})")


class GetRequestBuilder(RequestBuilder):
    @classmethod
    def from_request_builder(cls, builder: RequestBuilder):
        result = cls(builder.session, builder.path)
        result.json = builder.json
        result.http_method = builder.http_method
        return result

    def order(self, column: str, *, desc=False, nullsfirst=False):
        self.session.params.setdefault("order", []).append(
            f"{column}{'.desc' if desc else ''}{'.nullsfirst' if nullsfirst else ''}"
        )
        return self

    def limit(self, size: int, *, start=0):
        self.session.headers["Range-Unit"] = "items"
        self.session.headers["Range"] = f"{start}-{start + size - 1}"
        return self

    def range(self, start: int, end: int):
        self.session.headers["Range-Unit"] = "items"
        self.session.headers["Range"] = f"{start}-{end - 1}"
        return self

    def single(self):
        self.session.headers["Accept"] = "application/vnd.pgrst.object+json"
        return self

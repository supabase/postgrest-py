from typing import Iterable, Tuple

from deprecation import deprecated
from httpx import AsyncClient

from postgrest_py.utils import sanitize_param, sanitize_pattern_param
from postgrest_py.__version__ import __version__


class RequestBuilder:
    def __init__(self, session: AsyncClient, path: str):
        self.session = session
        self.path = path

    def select(self, *columns: str):
        self.session.params["select"] = ",".join(columns)
        return SelectRequestBuilder(self.session, self.path, "GET", {})

    def insert(self, json: dict, *, upsert=False):
        self.session.headers[
            "Prefer"
        ] = f"return=representation{',resolution=merge-duplicates' if upsert else ''}"
        return QueryRequestBuilder(self.session, self.path, "POST", json)

    def update(self, json: dict):
        self.session.headers["Prefer"] = "return=representation"
        return FilterRequestBuilder(self.session, self.path, "PATCH", json)

    def delete(self):
        return FilterRequestBuilder(self.session, self.path, "DELETE", {})


class QueryRequestBuilder:
    def __init__(self, session: AsyncClient, path: str, http_method: str, json: dict):
        self.session = session
        self.path = path
        self.http_method = http_method
        self.json = json

    async def execute(self):
        r = await self.session.request(self.http_method, self.path, json=self.json)
        return r.json()


class FilterRequestBuilder(QueryRequestBuilder):
    def __init__(self, session: AsyncClient, path: str, http_method: str, json: dict):
        super().__init__(session, path, http_method, json)

        self.negate_next = False

    @property
    def not_(self):
        self.negate_next = True
        return self

    def filter(self, column: str, operator: str, criteria: str):
        """Either filter in or filter out based on Self.negate_next."""
        if self.negate_next is True:
            self.negate_next = False
            operator = f"not.{operator}"
        key, val = sanitize_param(column), f"{operator}.{criteria}"
        if key in self.session.params:
            self.session.params.update({key: self.session.params.get_list(key) + [val]})
        else:
            self.session.params[key] = val
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


class SelectRequestBuilder(FilterRequestBuilder):
    def __init__(self, session: AsyncClient, path: str, http_method: str, json: dict):
        super().__init__(session, path, http_method, json)

    def order(self, column: str, *, desc=False, nullsfirst=False):
        self.session.params[
            "order"
        ] = f"{column}{'.desc' if desc else ''}{'.nullsfirst' if nullsfirst else ''}"

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


class GetRequestBuilder(SelectRequestBuilder):
    """Alias to SelectRequestBuilder."""

    @deprecated("0.4.0", "1.0.0", __version__, "Use SelectRequestBuilder instead")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

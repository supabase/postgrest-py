import re
import sys
from typing import Any, Dict, Iterable, Optional, Tuple, Union

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

from postgrest_py.utils import AsyncClient, sanitize_param, sanitize_pattern_param

CountMethod = Union[Literal["exact"], Literal["planned"], Literal["estimated"]]


class AsyncRequestBuilder:
    def __init__(self, session: AsyncClient, path: str):
        self.session = session
        self.path = path

    def select(self, *columns: str, count: Optional[CountMethod] = None):
        if columns:
            method = "GET"
            self.session.params = self.session.params.set("select", ",".join(columns))
        else:
            method = "HEAD"

        if count:
            self.session.headers["Prefer"] = f"count={count}"

        return AsyncSelectRequestBuilder(self.session, self.path, method, {})

    def insert(self, json: dict, *, count: Optional[CountMethod] = None, upsert=False):
        prefer_headers = ["return=representation"]
        if count:
            prefer_headers.append(f"count={count}")
        if upsert:
            prefer_headers.append("resolution=merge-duplicates")
        self.session.headers["prefer"] = ",".join(prefer_headers)
        return AsyncQueryRequestBuilder(self.session, self.path, "POST", json)

    def update(self, json: dict, *, count: Optional[CountMethod] = None):
        prefer_headers = ["return=representation"]
        if count:
            prefer_headers.append(f"count={count}")
        self.session.headers["prefer"] = ",".join(prefer_headers)
        return AsyncFilterRequestBuilder(self.session, self.path, "PATCH", json)

    def delete(self, *, count: Optional[CountMethod] = None):
        prefer_headers = ["return=representation"]
        if count:
            prefer_headers.append(f"count={count}")
        self.session.headers["prefer"] = ",".join(prefer_headers)
        return AsyncFilterRequestBuilder(self.session, self.path, "DELETE", {})


class AsyncQueryRequestBuilder:
    def __init__(self, session: AsyncClient, path: str, http_method: str, json: dict):
        self.session = session
        self.path = path
        self.http_method = http_method
        self.json = json

    async def execute(self) -> Tuple[Any, Optional[int]]:
        r = await self.session.request(self.http_method, self.path, json=self.json)

        count = None
        try:
            count_header_match = re.search(
                "count=(exact|planned|estimated)", self.session.headers["prefer"]
            )
            content_range = r.headers["content-range"].split("/")
            if count_header_match and len(content_range) >= 2:
                count = int(content_range[1])
        except KeyError:
            ...

        return r.json(), count


class AsyncFilterRequestBuilder(AsyncQueryRequestBuilder):
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
        self.session.params = self.session.params.add(key, val)
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

    def match(self, query: Dict[str, Any]):
        updated_query = None
        for key in query.keys():
            value = query.get(key, "")
            updated_query = self.eq(key, value)
        return updated_query


class AsyncSelectRequestBuilder(AsyncFilterRequestBuilder):
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

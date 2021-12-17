import re
import sys
from typing import Any, Dict, Iterable, Optional, Tuple, Union

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal

from httpx import Response

from postgrest_py.__version__ import __version__
from postgrest_py.utils import (
    AsyncClient,
    SyncClient,
    sanitize_param,
    sanitize_pattern_param,
)

CountMethod = Union[Literal["exact"], Literal["planned"], Literal["estimated"]]


def pre_select(
    session: Union[AsyncClient, SyncClient],
    path: str,
    *columns: str,
    count: Optional[CountMethod] = None,
) -> Tuple[str, dict]:
    if columns:
        method = "GET"
        session.params = session.params.set("select", ",".join(columns))
    else:
        method = "HEAD"
    if count:
        session.headers["Prefer"] = f"count={count}"
    return method, {}


def pre_insert(
    session: Union[AsyncClient, SyncClient],
    path: str,
    json: dict,
    *,
    count: Optional[CountMethod] = None,
    upsert=False,
) -> Tuple[str, dict]:
    prefer_headers = ["return=representation"]
    if count:
        prefer_headers.append(f"count={count}")
    if upsert:
        prefer_headers.append("resolution=merge-duplicates")
    session.headers["prefer"] = ",".join(prefer_headers)
    return "POST", json


def pre_update(
    session: Union[AsyncClient, SyncClient],
    path: str,
    json: dict,
    *,
    count: Optional[CountMethod] = None,
) -> Tuple[str, dict]:
    prefer_headers = ["return=representation"]
    if count:
        prefer_headers.append(f"count={count}")
    session.headers["prefer"] = ",".join(prefer_headers)
    return "PATCH", json


def pre_delete(
    session: Union[AsyncClient, SyncClient],
    path: str,
    *,
    count: Optional[CountMethod] = None,
) -> Tuple[str, dict]:
    prefer_headers = ["return=representation"]
    if count:
        prefer_headers.append(f"count={count}")
    session.headers["prefer"] = ",".join(prefer_headers)
    return "DELETE", {}


def process_response(
    session: Union[AsyncClient, SyncClient],
    r: Response,
) -> Tuple[Any, Optional[int]]:
    count = None
    try:
        count_header_match = re.search(
            "count=(exact|planned|estimated)", session.headers["prefer"]
        )
        content_range = r.headers["content-range"].split("/")
        if count_header_match and len(content_range) >= 2:
            count = int(content_range[1])
    except KeyError:
        pass
    return r.json(), count


class BaseFilterRequestBuilder:
    def __init__(self, session: Union[AsyncClient, SyncClient]):
        self.session = session
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
        return self.filter(column, "cs", f"{{{values}}}")

    def cd(self, column: str, values: Iterable[str]):
        values = map(sanitize_param, values)
        values = ",".join(values)
        return self.filter(column, "cd", f"{{{values}}}")

    def ov(self, column: str, values: Iterable[str]):
        values = map(sanitize_param, values)
        values = ",".join(values)
        return self.filter(column, "ov", f"{{{values}}}")

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


class BaseSelectRequestBuilder(BaseFilterRequestBuilder):
    def __init__(self, session: Union[AsyncClient, SyncClient]):
        BaseFilterRequestBuilder.__init__(self, session)

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

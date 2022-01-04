from re import search
from typing import Any, Dict, Iterable, Optional, Tuple, Union

from httpx import Response

from postgrest_py.types import CountMethod, Filters, RequestMethod, ReturnMethod
from postgrest_py.utils import (
    AsyncClient,
    SyncClient,
    sanitize_param,
    sanitize_pattern_param,
)


def pre_select(
    session: Union[AsyncClient, SyncClient],
    path: str,
    *columns: str,
    count: Optional[CountMethod] = None,
) -> Tuple[RequestMethod, dict]:
    if columns:
        method = RequestMethod.GET
        session.params = session.params.set("select", ",".join(columns))
    else:
        method = RequestMethod.HEAD
    if count:
        session.headers["Prefer"] = f"count={count}"
    return method, {}


def pre_insert(
    session: Union[AsyncClient, SyncClient],
    path: str,
    json: dict,
    *,
    count: Optional[CountMethod],
    returning: ReturnMethod,
    upsert: bool,
) -> Tuple[RequestMethod, dict]:
    prefer_headers = [f"return={returning}"]
    if count:
        prefer_headers.append(f"count={count}")
    if upsert:
        prefer_headers.append("resolution=merge-duplicates")
    session.headers["prefer"] = ",".join(prefer_headers)
    return RequestMethod.POST, json


def pre_upsert(
    session: Union[AsyncClient, SyncClient],
    path: str,
    json: dict,
    *,
    count: Optional[CountMethod],
    returning: ReturnMethod,
    ignore_duplicates: bool,
) -> Tuple[RequestMethod, dict]:
    prefer_headers = ["return=representation"]
    if count:
        prefer_headers.append(f"count={count}")
    resolution = "ignore" if ignore_duplicates else "merge"
    prefer_headers.append(f"resolution={resolution}-duplicates")
    session.headers["prefer"] = ",".join(prefer_headers)
    return RequestMethod.POST, json


def pre_update(
    session: Union[AsyncClient, SyncClient],
    path: str,
    json: dict,
    *,
    count: Optional[CountMethod],
    returning: ReturnMethod,
) -> Tuple[RequestMethod, dict]:
    prefer_headers = [f"return={returning}"]
    if count:
        prefer_headers.append(f"count={count}")
    session.headers["prefer"] = ",".join(prefer_headers)
    return RequestMethod.PATCH, json


def pre_delete(
    session: Union[AsyncClient, SyncClient],
    path: str,
    *,
    count: Optional[CountMethod],
    returning: ReturnMethod,
) -> Tuple[RequestMethod, dict]:
    prefer_headers = [f"return={returning}"]
    if count:
        prefer_headers.append(f"count={count}")
    session.headers["prefer"] = ",".join(prefer_headers)
    return RequestMethod.DELETE, {}


def process_response(
    session: Union[AsyncClient, SyncClient],
    r: Response,
) -> Tuple[Any, Optional[int]]:
    count = None
    prefer_header = session.headers.get("prefer")
    if prefer_header:
        pattern = f"count=({'|'.join([cm.value for cm in CountMethod])})"
        count_header_match = search(pattern, prefer_header)
        content_range_header = r.headers.get("content-range")
        if count_header_match and content_range_header:
            content_range = content_range_header.split("/")
            if len(content_range) >= 2:
                count = int(content_range[1])
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
        """Either filter in or filter out based on `self.negate_next.`"""
        if self.negate_next is True:
            self.negate_next = False
            operator = f"{Filters.NOT}.{operator}"
        key, val = sanitize_param(column), f"{operator}.{criteria}"
        self.session.params = self.session.params.add(key, val)
        return self

    def eq(self, column: str, value: Any):
        return self.filter(column, Filters.EQ, sanitize_param(value))

    def neq(self, column: str, value: Any):
        return self.filter(column, Filters.NEQ, sanitize_param(value))

    def gt(self, column: str, value: Any):
        return self.filter(column, Filters.GT, sanitize_param(value))

    def gte(self, column: str, value: Any):
        return self.filter(column, Filters.GTE, sanitize_param(value))

    def lt(self, column: str, value: Any):
        return self.filter(column, Filters.LT, sanitize_param(value))

    def lte(self, column: str, value: Any):
        return self.filter(column, Filters.LTE, sanitize_param(value))

    def is_(self, column: str, value: Any):
        return self.filter(column, Filters.IS, sanitize_param(value))

    def like(self, column: str, pattern: Any):
        return self.filter(column, Filters.LIKE, sanitize_pattern_param(pattern))

    def ilike(self, column: str, pattern: Any):
        return self.filter(column, Filters.ILIKE, sanitize_pattern_param(pattern))

    def fts(self, column: str, query: Any):
        return self.filter(column, Filters.FTS, sanitize_param(query))

    def plfts(self, column: str, query: Any):
        return self.filter(column, Filters.PLFTS, sanitize_param(query))

    def phfts(self, column: str, query: Any):
        return self.filter(column, Filters.PHFTS, sanitize_param(query))

    def wfts(self, column: str, query: Any):
        return self.filter(column, Filters.WFTS, sanitize_param(query))

    def in_(self, column: str, values: Iterable[Any]):
        values = map(sanitize_param, values)
        values = ",".join(values)
        return self.filter(column, Filters.IN, f"({values})")

    def cs(self, column: str, values: Iterable[Any]):
        values = map(sanitize_param, values)
        values = ",".join(values)
        return self.filter(column, Filters.CS, f"{{{values}}}")

    def cd(self, column: str, values: Iterable[Any]):
        values = map(sanitize_param, values)
        values = ",".join(values)
        return self.filter(column, Filters.CD, f"{{{values}}}")

    def ov(self, column: str, values: Iterable[Any]):
        values = map(sanitize_param, values)
        values = ",".join(values)
        return self.filter(column, Filters.OV, f"{{{values}}}")

    def sl(self, column: str, range: Tuple[int, int]):
        return self.filter(column, Filters.SL, f"({range[0]},{range[1]})")

    def sr(self, column: str, range: Tuple[int, int]):
        return self.filter(column, Filters.SR, f"({range[0]},{range[1]})")

    def nxl(self, column: str, range: Tuple[int, int]):
        return self.filter(column, Filters.NXL, f"({range[0]},{range[1]})")

    def nxr(self, column: str, range: Tuple[int, int]):
        return self.filter(column, Filters.NXR, f"({range[0]},{range[1]})")

    def adj(self, column: str, range: Tuple[int, int]):
        return self.filter(column, Filters.ADJ, f"({range[0]},{range[1]})")

    def match(self, query: Dict[str, Any]):
        updated_query = None
        for key in query:
            value = query.get(key, "")
            updated_query = self.eq(key, value)
        return updated_query


class BaseSelectRequestBuilder(BaseFilterRequestBuilder):
    def __init__(self, session: Union[AsyncClient, SyncClient]):
        BaseFilterRequestBuilder.__init__(self, session)

    def order(self, column: str, *, desc=False, nullsfirst=False):
        self.session.params.add(
            "order",
            f"{column}{'.desc' if desc else ''}{'.nullsfirst' if nullsfirst else ''}",
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

from __future__ import annotations

from typing import Optional

from ..base_request_builder import (
    APIResponse,
    BaseFilterRequestBuilder,
    BaseSelectRequestBuilder,
    CountMethod,
    pre_delete,
    pre_insert,
    pre_select,
    pre_update,
    pre_upsert,
)
from ..exceptions import APIError
from ..types import ReturnMethod
from ..utils import SyncClient


class SyncQueryRequestBuilder:
    def __init__(
        self,
        session: SyncClient,
        path: str,
        http_method: str,
        json: dict,
    ) -> None:
        self.session = session
        self.path = path
        self.http_method = http_method
        self.json = json

    def execute(self) -> APIResponse:
        r = self.session.request(
            self.http_method,
            self.path,
            json=self.json,
        )
        try:
            return APIResponse.from_http_request_response(r)
        except ValueError as e:
            raise APIError(r.json()) from e


# ignoring type checking as a workaround for https://github.com/python/mypy/issues/9319
class SyncFilterRequestBuilder(BaseFilterRequestBuilder, SyncQueryRequestBuilder):  # type: ignore
    def __init__(
        self,
        session: SyncClient,
        path: str,
        http_method: str,
        json: dict,
    ) -> None:
        BaseFilterRequestBuilder.__init__(self, session)
        SyncQueryRequestBuilder.__init__(self, session, path, http_method, json)


# ignoring type checking as a workaround for https://github.com/python/mypy/issues/9319
class SyncSelectRequestBuilder(BaseSelectRequestBuilder, SyncQueryRequestBuilder):  # type: ignore
    def __init__(
        self,
        session: SyncClient,
        path: str,
        http_method: str,
        json: dict,
    ) -> None:
        BaseSelectRequestBuilder.__init__(self, session)
        SyncQueryRequestBuilder.__init__(self, session, path, http_method, json)


class SyncRequestBuilder:
    def __init__(self, session: SyncClient, path: str) -> None:
        self.session = session
        self.path = path

    def select(
        self,
        *columns: str,
        count: Optional[CountMethod] = None,
    ) -> SyncSelectRequestBuilder:
        method, json = pre_select(self.session, *columns, count=count)
        return SyncSelectRequestBuilder(self.session, self.path, method, json)

    def insert(
        self,
        json: dict,
        *,
        count: Optional[CountMethod] = None,
        returning: ReturnMethod = ReturnMethod.representation,
        upsert=False,
    ) -> SyncQueryRequestBuilder:
        method, json = pre_insert(
            self.session,
            json,
            count=count,
            returning=returning,
            upsert=upsert,
        )
        return SyncQueryRequestBuilder(self.session, self.path, method, json)

    def upsert(
        self,
        json: dict,
        *,
        count: Optional[CountMethod] = None,
        returning: ReturnMethod = ReturnMethod.representation,
        ignore_duplicates=False,
    ) -> SyncQueryRequestBuilder:
        method, json = pre_upsert(
            self.session,
            json,
            count=count,
            returning=returning,
            ignore_duplicates=ignore_duplicates,
        )
        return SyncQueryRequestBuilder(self.session, self.path, method, json)

    def update(
        self,
        json: dict,
        *,
        count: Optional[CountMethod] = None,
        returning: ReturnMethod = ReturnMethod.representation,
    ) -> SyncFilterRequestBuilder:
        method, json = pre_update(
            self.session,
            json,
            count=count,
            returning=returning,
        )
        return SyncFilterRequestBuilder(self.session, self.path, method, json)

    def delete(
        self,
        *,
        count: Optional[CountMethod] = None,
        returning: ReturnMethod = ReturnMethod.representation,
    ) -> SyncFilterRequestBuilder:
        method, json = pre_delete(
            self.session,
            count=count,
            returning=returning,
        )
        return SyncFilterRequestBuilder(self.session, self.path, method, json)

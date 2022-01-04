from typing import Any, Optional, Tuple

from postgrest_py.base_request_builder import (
    BaseFilterRequestBuilder,
    BaseSelectRequestBuilder,
    CountMethod,
    pre_delete,
    pre_insert,
    pre_select,
    pre_update,
    pre_upsert,
    process_response,
)
from postgrest_py.types import ReturnMethod
from postgrest_py.utils import SyncClient


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

    def execute(self) -> Tuple[Any, Optional[int]]:
        r = self.session.request(
            self.http_method,
            self.path,
            json=self.json,
        )
        return process_response(self.session, r)


class SyncFilterRequestBuilder(BaseFilterRequestBuilder, SyncQueryRequestBuilder):
    def __init__(
        self,
        session: SyncClient,
        path: str,
        http_method: str,
        json: dict,
    ) -> None:
        BaseFilterRequestBuilder.__init__(self, session)
        SyncQueryRequestBuilder.__init__(self, session, path, http_method, json)


class SyncSelectRequestBuilder(BaseSelectRequestBuilder, SyncQueryRequestBuilder):
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
        method, json = pre_select(self.session, self.path, *columns, count=count)
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
            self.path,
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
            self.path,
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
            self.path,
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
            self.path,
            count=count,
            returning=returning,
        )
        return SyncFilterRequestBuilder(self.session, self.path, method, json)

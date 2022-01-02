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
from postgrest_py.utils import AsyncClient


class AsyncQueryRequestBuilder:
    def __init__(
        self,
        session: AsyncClient,
        path: str,
        http_method: str,
        json: dict,
    ) -> None:
        self.session = session
        self.path = path
        self.http_method = http_method
        self.json = json

    async def execute(self) -> Tuple[Any, Optional[int]]:
        r = await self.session.request(
            self.http_method,
            self.path,
            json=self.json,
        )
        return process_response(self.session, r)


class AsyncFilterRequestBuilder(BaseFilterRequestBuilder, AsyncQueryRequestBuilder):
    def __init__(
        self,
        session: AsyncClient,
        path: str,
        http_method: str,
        json: dict,
    ) -> None:
        BaseFilterRequestBuilder.__init__(self, session)
        AsyncQueryRequestBuilder.__init__(self, session, path, http_method, json)


class AsyncSelectRequestBuilder(BaseSelectRequestBuilder, AsyncQueryRequestBuilder):
    def __init__(
        self,
        session: AsyncClient,
        path: str,
        http_method: str,
        json: dict,
    ) -> None:
        BaseSelectRequestBuilder.__init__(self, session)
        AsyncQueryRequestBuilder.__init__(self, session, path, http_method, json)


class AsyncRequestBuilder:
    def __init__(self, session: AsyncClient, path: str) -> None:
        self.session = session
        self.path = path

    def select(
        self,
        *columns: str,
        count: Optional[CountMethod] = None,
    ) -> AsyncSelectRequestBuilder:
        method, json = pre_select(self.session, self.path, *columns, count=count)
        return AsyncSelectRequestBuilder(self.session, self.path, method, json)

    def insert(
        self,
        json: dict,
        *,
        count: Optional[CountMethod] = None,
        returning: ReturnMethod = ReturnMethod.representation,
        upsert=False,
    ) -> AsyncQueryRequestBuilder:
        method, json = pre_insert(
            self.session,
            self.path,
            json,
            count=count,
            returning=returning,
            upsert=upsert,
        )
        return AsyncQueryRequestBuilder(self.session, self.path, method, json)

    def upsert(
        self,
        json: dict,
        *,
        count: Optional[CountMethod] = None,
        returning: ReturnMethod = ReturnMethod.representation,
        ignore_duplicates=False,
    ) -> AsyncQueryRequestBuilder:
        method, json = pre_upsert(
            self.session,
            self.path,
            json,
            count=count,
            returning=returning,
            ignore_duplicates=ignore_duplicates,
        )
        return AsyncQueryRequestBuilder(self.session, self.path, method, json)

    def update(
        self,
        json: dict,
        *,
        count: Optional[CountMethod] = None,
        returning: ReturnMethod = ReturnMethod.representation,
    ) -> AsyncFilterRequestBuilder:
        method, json = pre_update(
            self.session,
            self.path,
            json,
            count=count,
            returning=returning,
        )
        return AsyncFilterRequestBuilder(self.session, self.path, method, json)

    def delete(
        self,
        *,
        count: Optional[CountMethod] = None,
        returning: ReturnMethod = ReturnMethod.representation,
    ) -> AsyncFilterRequestBuilder:
        method, json = pre_delete(
            self.session,
            self.path,
            count=count,
            returning=returning,
        )
        return AsyncFilterRequestBuilder(self.session, self.path, method, json)

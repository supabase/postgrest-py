from __future__ import annotations

from typing import Optional

from httpx import Headers, QueryParams
from pydantic import ValidationError

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
        """Execute the query.

        .. tip::
            This is the last method called, after the query is built.

        Returns:
            :class:`APIResponse`

        Raises:
            :class:`APIError`
        """
        r = self.session.request(
            self.http_method,
            self.path,
            json=self.json,
        )

        key = self.session.headers.get("apiKey")
        auth = self.session.headers.get("Authorization")
        headers = Headers()

        if key:
            headers["apiKey"] = key
        if auth:
            headers["Authorization"] = auth
        # remove the params and headers that were set by the query
        self.session.params = QueryParams()
        self.session.headers = headers

        try:
            return APIResponse.from_http_request_response(r)
        except ValidationError as e:
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
        """Run a SELECT query.

        Args:
            *columns: The names of the columns to fetch.
            count: The method to use to get the count of rows returned.
        Returns:
            :class:`AsyncSelectRequestBuilder`
        """
        method, json = pre_select(self.session, *columns, count=count)
        return SyncSelectRequestBuilder(self.session, self.path, method, json)

    def insert(
        self,
        json: dict,
        *,
        count: Optional[CountMethod] = None,
        returning: ReturnMethod = ReturnMethod.representation,
        upsert: bool = False,
    ) -> SyncQueryRequestBuilder:
        """Run an INSERT query.

        Args:
            json: The row to be inserted.
            count: The method to use to get the count of rows returned.
            returning: Either 'minimal' or 'representation'
            upsert: Whether the query should be an upsert.
        Returns:
            :class:`AsyncQueryRequestBuilder`
        """
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
        ignore_duplicates: bool = False,
    ) -> SyncQueryRequestBuilder:
        """Run an upsert (INSERT ... ON CONFLICT DO UPDATE) query.

        Args:
            json: The row to be inserted.
            count: The method to use to get the count of rows returned.
            returning: Either 'minimal' or 'representation'
            ignore_duplicates: Whether duplicate rows should be ignored.
        Returns:
            :class:`AsyncQueryRequestBuilder`
        """
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
        """Run an UPDATE query.

        Args:
            json: The updated fields.
            count: The method to use to get the count of rows returned.
            returning: Either 'minimal' or 'representation'
        Returns:
            :class:`AsyncFilterRequestBuilder`
        """
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
        """Run a DELETE query.

        Args:
            count: The method to use to get the count of rows returned.
            returning: Either 'minimal' or 'representation'
        Returns:
            :class:`AsyncFilterRequestBuilder`
        """
        method, json = pre_delete(
            self.session,
            count=count,
            returning=returning,
        )
        return SyncFilterRequestBuilder(self.session, self.path, method, json)

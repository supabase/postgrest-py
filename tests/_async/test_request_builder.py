from typing import Any, Dict, List

import pytest

from postgrest_py import AsyncRequestBuilder
from postgrest_py.base_request_builder import APIResponse
from postgrest_py.types import CountMethod
from postgrest_py.utils import AsyncClient


@pytest.fixture
async def request_builder():
    async with AsyncClient() as client:
        yield AsyncRequestBuilder(client, "/example_table")


def test_constructor(request_builder):
    assert request_builder.path == "/example_table"


class TestSelect:
    def test_select(self, request_builder: AsyncRequestBuilder):
        builder = request_builder.select("col1", "col2")

        assert builder.session.params["select"] == "col1,col2"
        assert builder.session.headers.get("prefer") is None
        assert builder.http_method == "GET"
        assert builder.json == {}

    def test_select_with_count(self, request_builder: AsyncRequestBuilder):
        builder = request_builder.select(count=CountMethod.exact)

        assert builder.session.params.get("select") is None
        assert builder.session.headers["prefer"] == "count=exact"
        assert builder.http_method == "HEAD"
        assert builder.json == {}


class TestInsert:
    def test_insert(self, request_builder: AsyncRequestBuilder):
        builder = request_builder.insert({"key1": "val1"})

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation"
        ]
        assert builder.http_method == "POST"
        assert builder.json == {"key1": "val1"}

    def test_insert_with_count(self, request_builder: AsyncRequestBuilder):
        builder = request_builder.insert({"key1": "val1"}, count=CountMethod.exact)

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation",
            "count=exact",
        ]
        assert builder.http_method == "POST"
        assert builder.json == {"key1": "val1"}

    def test_insert_with_upsert(self, request_builder: AsyncRequestBuilder):
        builder = request_builder.insert({"key1": "val1"}, upsert=True)

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation",
            "resolution=merge-duplicates",
        ]
        assert builder.http_method == "POST"
        assert builder.json == {"key1": "val1"}

    def test_upsert(self, request_builder: AsyncRequestBuilder):
        builder = request_builder.upsert({"key1": "val1"})

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation",
            "resolution=merge-duplicates",
        ]
        assert builder.http_method == "POST"
        assert builder.json == {"key1": "val1"}


class TestUpdate:
    def test_update(self, request_builder: AsyncRequestBuilder):
        builder = request_builder.update({"key1": "val1"})

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation"
        ]
        assert builder.http_method == "PATCH"
        assert builder.json == {"key1": "val1"}

    def test_update_with_count(self, request_builder: AsyncRequestBuilder):
        builder = request_builder.update({"key1": "val1"}, count=CountMethod.exact)

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation",
            "count=exact",
        ]
        assert builder.http_method == "PATCH"
        assert builder.json == {"key1": "val1"}


class TestDelete:
    def test_delete(self, request_builder: AsyncRequestBuilder):
        builder = request_builder.delete()

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation"
        ]
        assert builder.http_method == "DELETE"
        assert builder.json == {}

    def test_delete_with_count(self, request_builder: AsyncRequestBuilder):
        builder = request_builder.delete(count=CountMethod.exact)

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation",
            "count=exact",
        ]
        assert builder.http_method == "DELETE"
        assert builder.json == {}


@pytest.fixture
def api_response_with_error() -> dict[str, Any]:
    return {
        "message": "Route GET:/countries?select=%2A not found",
        "error": "Not Found",
        "statusCode": 404,
    }


@pytest.fixture
def api_response() -> List[Dict[str, Any]]:
    return [
        {
            "id": 1,
            "name": "Bonaire, Sint Eustatius and Saba",
            "iso2": "BQ",
            "iso3": "BES",
            "local_name": None,
            "continent": None,
        },
        {
            "id": 2,
            "name": "Curaçao",
            "iso2": "CW",
            "iso3": "CUW",
            "local_name": None,
            "continent": None,
        },
    ]


@pytest.fixture
def content_range_header_with_count():
    return "0-1/2"


@pytest.fixture
def content_range_header_without_count():
    return "0-1"


@pytest.fixture
def prefer_header_with_count():
    return "count=exact"


@pytest.fixture
def prefer_header_without_count():
    return "random prefer header"


class TestApiResponse:
    def test_response_raises_when_api_error(
        self, api_response_with_error: Dict[str, Any]
    ):
        with pytest.raises(ValueError):
            APIResponse(data=api_response_with_error)

    def test_parses_valid_response_only_data(self, api_response: List[Dict[str, Any]]):
        result = APIResponse(data=api_response)
        assert result.data == api_response

    def test_parses_valid_response_data_and_count(
        self, api_response: List[Dict[str, Any]]
    ):
        count = len(api_response)
        result = APIResponse(data=api_response, count=count)
        assert result.data == api_response
        assert result.count == count

    def test_get_count_from_content_range_header_with_count(
        self, content_range_header_with_count
    ):
        assert (
            APIResponse.get_count_from_content_range_header(
                content_range_header_with_count
            )
            == 2
        )

    def test_get_count_from_content_range_header_without_count(
        self, content_range_header_without_count
    ):
        assert (
            APIResponse.get_count_from_content_range_header(
                content_range_header_without_count
            )
            is None
        )

    def test_is_count_in_prefer_header_true(self, prefer_header_with_count):
        assert APIResponse.is_count_in_prefer_header(prefer_header_with_count)

    def test_is_count_in_prefer_header_false(self, prefer_header_without_count):
        assert not APIResponse.is_count_in_prefer_header(prefer_header_without_count)

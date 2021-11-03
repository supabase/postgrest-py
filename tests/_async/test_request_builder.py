import pytest

from postgrest_py import AsyncRequestBuilder
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
        assert builder.session.headers.get("prefer") == None
        assert builder.http_method == "GET"
        assert builder.json == {}

    def test_select_with_count(self, request_builder: AsyncRequestBuilder):
        builder = request_builder.select(count="exact")

        assert builder.session.params.get("select") == None
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
        builder = request_builder.insert({"key1": "val1"}, count="exact")

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation",
            "count=exact",
        ]
        assert builder.http_method == "POST"
        assert builder.json == {"key1": "val1"}

    def test_upsert(self, request_builder: AsyncRequestBuilder):
        builder = request_builder.insert({"key1": "val1"}, upsert=True)

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
        builder = request_builder.update({"key1": "val1"}, count="exact")

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
        builder = request_builder.delete(count="exact")

        assert builder.session.headers.get_list("prefer", True) == [
            "return=representation",
            "count=exact",
        ]
        assert builder.http_method == "DELETE"
        assert builder.json == {}

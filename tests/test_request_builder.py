import pytest
from httpx import AsyncClient
from postgrest_py.request_builder import RequestBuilder


@pytest.fixture
async def request_builder():
    async with AsyncClient() as client:
        yield RequestBuilder(client, "/example_table")


def test_constructor(request_builder):
    assert request_builder.path == "/example_table"


class TestSelect:
    def test_select(self, request_builder: RequestBuilder):
        builder = request_builder.select("col1", "col2")

        assert builder.session.params["select"] == "col1,col2"
        assert builder.session.headers.get("prefer") == None
        assert builder.http_method == "GET"
        assert builder.json == {}

    def test_select_with_count(self, request_builder: RequestBuilder):
        builder = request_builder.select("col1", "col2", count="exact", head=True)

        assert builder.session.params["select"] == "col1,col2"
        assert builder.session.headers["prefer"] == "count=exact"
        assert builder.http_method == "HEAD"
        assert builder.json == {}


class TestInsert:
    def test_insert(self, request_builder):
        builder = request_builder.insert({"key1": "val1"})

        assert builder.session.headers["prefer"] == "return=representation"
        assert builder.http_method == "POST"
        assert builder.json == {"key1": "val1"}

    def test_upsert(self, request_builder):
        builder = request_builder.insert({"key1": "val1"}, upsert=True)

        assert (
            builder.session.headers["prefer"]
            == "return=representation,resolution=merge-duplicates"
        )
        assert builder.http_method == "POST"
        assert builder.json == {"key1": "val1"}


def test_update(request_builder):
    builder = request_builder.update({"key1": "val1"})

    assert builder.session.headers["prefer"] == "return=representation"
    assert builder.http_method == "PATCH"
    assert builder.json == {"key1": "val1"}


def test_delete(request_builder):
    builder = request_builder.delete()

    assert builder.http_method == "DELETE"
    assert builder.json == {}

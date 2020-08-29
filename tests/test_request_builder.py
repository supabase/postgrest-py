import pytest
from httpx import AsyncClient
from postgrest_py.request_builder import RequestBuilder


@pytest.fixture
async def request_builder():
    async with AsyncClient() as client:
        yield RequestBuilder(client, "/example_table")


@pytest.mark.asyncio
def test_constructor(request_builder):
    assert request_builder.path == "/example_table"
    assert request_builder.json == {}
    assert request_builder.http_method == "GET"
    assert request_builder.negate_next == False


def test_select(request_builder):
    request_builder.select("col1", "col2")

    assert request_builder.session.params["select"] == "col1,col2"
    assert request_builder.http_method == "GET"


class TestInsert:
    def test_insert(self, request_builder):
        request_builder.insert({"key1": "val1"})

        assert request_builder.session.headers["prefer"] == "return=representation"
        assert request_builder.json == {"key1": "val1"}
        assert request_builder.http_method == "POST"

    def test_upsert(self, request_builder):
        request_builder.insert({"key1": "val1"}, upsert=True)

        assert (
            request_builder.session.headers["prefer"]
            == "return=representation,resolution=merge-duplicates"
        )
        assert request_builder.json == {"key1": "val1"}
        assert request_builder.http_method == "POST"


def test_update(request_builder):
    request_builder.update({"key1": "val1"})

    assert request_builder.session.headers["prefer"] == "return=representation"
    assert request_builder.json == {"key1": "val1"}
    assert request_builder.http_method == "PATCH"


def test_delete(request_builder):
    request_builder.delete()

    assert request_builder.http_method == "DELETE"


@pytest.mark.asyncio
def test_not_(request_builder):
    request_builder.not_

    assert request_builder.negate_next == True

import pytest
from httpx import AsyncClient
from postgrest_py.request_builder import FilterRequestBuilder


@pytest.fixture
async def filter_request_builder():
    async with AsyncClient() as client:
        yield FilterRequestBuilder(client, "/example_table", "GET", {})


def test_constructor(filter_request_builder):
    builder = filter_request_builder

    assert builder.path == "/example_table"
    assert builder.http_method == "GET"
    assert builder.json == {}
    assert builder.negate_next == False


def test_not_(filter_request_builder):
    builder = filter_request_builder.not_

    assert builder.negate_next == True


def test_filter(filter_request_builder):
    builder = filter_request_builder.filter(":col.name", "eq", "val")

    assert builder.session.params['":col.name"'] == "eq.val"


def test_multivalued_param(filter_request_builder):
    builder = filter_request_builder.lte("x", "a").gte("x", "b")

    assert str(builder.session.params) == "x=lte.a&x=gte.b"

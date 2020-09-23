import pytest
from httpx import AsyncClient
from postgrest_py.request_builder import QueryRequestBuilder


@pytest.fixture
async def query_request_builder():
    async with AsyncClient() as client:
        yield QueryRequestBuilder(client, "/example_table", "GET", {})


def test_constructor(query_request_builder):
    builder = query_request_builder

    assert builder.path == "/example_table"
    assert builder.http_method == "GET"
    assert builder.json == {}

import pytest
from postgrest_py.utils import AsyncClient
from postgrest_py import AsyncQueryRequestBuilder


@pytest.fixture
async def query_request_builder():
    async with AsyncClient() as client:
        yield AsyncQueryRequestBuilder(client, "/example_table", "GET", {})


def test_constructor(query_request_builder):
    builder = query_request_builder

    assert builder.path == "/example_table"
    assert builder.http_method == "GET"
    assert builder.json == {}

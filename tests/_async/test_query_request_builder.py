import pytest

from postgrest import AsyncQueryRequestBuilder
from postgrest.utils import AsyncClient


@pytest.fixture
async def query_request_builder():
    async with AsyncClient() as client:
        yield AsyncQueryRequestBuilder(client, "/example_table", "GET", {})


def test_constructor(query_request_builder):
    builder = query_request_builder

    assert builder.path == "/example_table"
    assert builder.http_method == "GET"
    assert builder.json == {}

import pytest
from postgrest_py.utils import SyncClient
from postgrest_py import SyncQueryRequestBuilder


@pytest.fixture
def query_request_builder():
    with SyncClient() as client:
        yield SyncQueryRequestBuilder(client, "/example_table", "GET", {})


def test_constructor(query_request_builder):
    builder = query_request_builder

    assert builder.path == "/example_table"
    assert builder.http_method == "GET"
    assert builder.json == {}

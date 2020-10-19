import pytest
from postgrest_py import PostgrestClient


@pytest.fixture
async def postgrest_client():
    async with PostgrestClient("https://example.com") as client:
        yield client


@pytest.mark.asyncio
def test_constructor(postgrest_client):
    session = postgrest_client.session

    assert session.base_url == "https://example.com"
    default_headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "accept-profile": "public",
        "content-profile": "public",
    }
    assert default_headers.items() <= session.headers.items()


class TestAuth:
    @pytest.mark.asyncio
    def test_auth_token(self, postgrest_client):
        postgrest_client.auth("s3cr3t")
        session = postgrest_client.session

        assert session.headers["Authorization"] == "Bearer s3cr3t"

    @pytest.mark.asyncio
    def test_auth_basic(self, postgrest_client):
        postgrest_client.auth(None, username="admin", password="s3cr3t")
        session = postgrest_client.session

        assert session.auth == ("admin", "s3cr3t")


@pytest.mark.asyncio
def test_schema(postgrest_client: PostgrestClient):
    postgrest_client.schema("private")
    session = postgrest_client.session
    subheaders = {
        "accept-profile": "private",
        "content-profile": "private",
    }

    assert subheaders.items() < dict(session.headers).items()

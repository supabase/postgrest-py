import pytest
from httpx import BasicAuth, Headers
from postgrest_py import AsyncPostgrestClient


@pytest.fixture
async def postgrest_client():
    async with AsyncPostgrestClient("https://example.com") as client:
        yield client


class TestConstructor:
    @pytest.mark.asyncio
    def test_simple(self, postgrest_client: AsyncPostgrestClient):
        session = postgrest_client.session

        assert session.base_url == "https://example.com"
        headers = Headers(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Accept-Profile": "public",
                "Content-Profile": "public",
            }
        )
        assert session.headers.items() >= headers.items()

    @pytest.mark.asyncio
    async def test_custom_headers(self):
        async with AsyncPostgrestClient(
            "https://example.com", schema="pub", headers={"Custom-Header": "value"}
        ) as client:
            session = client.session

            assert session.base_url == "https://example.com"
            headers = Headers(
                {
                    "Accept-Profile": "pub",
                    "Content-Profile": "pub",
                    "Custom-Header": "value",
                }
            )
            assert session.headers.items() >= headers.items()


class TestAuth:
    @pytest.mark.asyncio
    def test_auth_token(self, postgrest_client: AsyncPostgrestClient):
        postgrest_client.auth("s3cr3t")
        session = postgrest_client.session

        assert session.headers["Authorization"] == "Bearer s3cr3t"

    @pytest.mark.asyncio
    def test_auth_basic(self, postgrest_client: AsyncPostgrestClient):
        postgrest_client.auth(None, username="admin", password="s3cr3t")
        session = postgrest_client.session

        assert isinstance(session.auth, BasicAuth)
        assert session.auth._auth_header == BasicAuth("admin", "s3cr3t")._auth_header


@pytest.mark.asyncio
def test_schema(postgrest_client: AsyncPostgrestClient):
    postgrest_client.schema("private")
    session = postgrest_client.session
    subheaders = {
        "accept-profile": "private",
        "content-profile": "private",
    }

    assert subheaders.items() < dict(session.headers).items()

import pytest
from httpx import BasicAuth, Headers
from postgrest_py import PostgrestClient


@pytest.fixture
def postgrest_client():
    with PostgrestClient("https://example.com") as client:
        yield client


class TestConstructor:
    def test_simple(self, postgrest_client: PostgrestClient):
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

    def test_custom_headers(self):
        with PostgrestClient(
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
    def test_auth_token(self, postgrest_client: PostgrestClient):
        postgrest_client.auth("s3cr3t")
        session = postgrest_client.session

        assert session.headers["Authorization"] == "Bearer s3cr3t"

    def test_auth_basic(self, postgrest_client: PostgrestClient):
        postgrest_client.auth(None, username="admin", password="s3cr3t")
        session = postgrest_client.session

        assert isinstance(session.auth, BasicAuth)
        assert session.auth._auth_header == BasicAuth("admin", "s3cr3t")._auth_header


def test_schema(postgrest_client: PostgrestClient):
    postgrest_client.schema("private")
    session = postgrest_client.session
    subheaders = {
        "accept-profile": "private",
        "content-profile": "private",
    }

    assert subheaders.items() < dict(session.headers).items()

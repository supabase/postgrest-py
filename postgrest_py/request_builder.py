from httpx import AsyncClient


class RequestBuilder:
    def __init__(self, session: AsyncClient, table: str) -> None:
        self.session = session
        self.path = f"/{table}"
        self.http_method = "GET"
        self.params = {}
        self.json = {}

    def select(self, columns: str) -> RequestBuilder:
        self.http_method = "GET"
        self.params["select"] = columns

    def insert(self, json: dict, *, upsert=False) -> RequestBuilder:
        self.http_method = "POST"
        self.session.headers[
            "Prefer"
        ] = f"return=representation{',resolution=merge-duplicates' if upsert else ''}"
        self.json = json

    def update(self, json: dict) -> RequestBuilder:
        self.http_method = "PATCH"
        self.session.headers["Prefer"] = "return=representation"
        self.json = json

    def delete(self) -> RequestBuilder:
        self.http_method = "DELETE"

from httpx import AsyncClient


class RequestBuilder:
    def __init__(self, session: AsyncClient, path: str) -> None:
        self.session = session
        self.path = path
        self.params = {}
        self.json = {}
        self.http_method = "GET"

    def select(self, columns: str) -> RequestBuilder:
        self.params["select"] = columns
        self.http_method = "GET"
        return self

    def insert(self, json: dict, *, upsert=False) -> RequestBuilder:
        self.session.headers[
            "Prefer"
        ] = f"return=representation{',resolution=merge-duplicates' if upsert else ''}"
        self.json = json
        self.http_method = "POST"
        return self

    def update(self, json: dict) -> RequestBuilder:
        self.session.headers["Prefer"] = "return=representation"
        self.json = json
        self.http_method = "PATCH"
        return self

    def delete(self) -> RequestBuilder:
        self.http_method = "DELETE"
        return self

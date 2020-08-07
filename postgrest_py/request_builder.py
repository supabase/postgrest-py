from httpx import AsyncClient


class RequestBuilder:
    def __init__(self, session: AsyncClient, path: str) -> None:
        self.session = session
        self.path = path
        self.json = {}
        self.http_method = "GET"

    def select(self, columns: str) -> GetRequestBuilder:
        self.session.params["select"] = columns
        self.http_method = "GET"
        return GetRequestBuilder.from_request_builder(self)

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


class GetRequestBuilder(RequestBuilder):
    @classmethod
    def from_request_builder(cls, builder: RequestBuilder) -> GetRequestBuilder:
        result = cls(builder.session, builder.path)
        result.json = builder.json
        result.http_method = builder.http_method
        return result

    def order(self, column: str, *, desc=False, nullsfirst=False) -> GetRequestBuilder:
        self.session.params[
            "order"
        ] = f"{column}{'.desc' if desc else ''}{'.nullsfirst' if nullsfirst else ''}"
        return self

    def limit(self, size: int, *, start=0) -> GetRequestBuilder:
        self.session.headers["Range-Unit"] = "items"
        self.session.headers["Range"] = f"{start}-{start + size - 1}"
        return self

    def range(self, start: int, end: int) -> GetRequestBuilder:
        self.session.headers["Range-Unit"] = "items"
        self.session.headers["Range"] = f"{start}-{end - 1}"
        return self

    def single(self) -> GetRequestBuilder:
        self.session.headers["Accept"] = "application/vnd.pgrst.object+json"
        return self

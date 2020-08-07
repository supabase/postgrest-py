from httpx import AsyncClient, Response


class RequestBuilder:
    def __init__(self, session: AsyncClient, path: str) -> None:
        self.session = session
        self.path = path
        self.json = {}
        self.http_method = "GET"

    def select(self, columns: str):
        self.session.params["select"] = columns
        self.http_method = "GET"
        return GetRequestBuilder.from_request_builder(self)

    def insert(self, json: dict, *, upsert=False):
        self.session.headers[
            "Prefer"
        ] = f"return=representation{',resolution=merge-duplicates' if upsert else ''}"
        self.json = json
        self.http_method = "POST"
        return self

    def update(self, json: dict):
        self.session.headers["Prefer"] = "return=representation"
        self.json = json
        self.http_method = "PATCH"
        return self

    def delete(self):
        self.http_method = "DELETE"
        return self

    async def execute(self) -> Response:
        r = await self.session.request(self.http_method, self.path, json=self.json)
        return r

    def filter_in(self, column: str, operator: str, criteria: str):
        self.session.params[column] = f"{operator}.{criteria}"
        return self

    def filter(self, column: str, operator: str, criteria: str):
        """Alias to Self.filter_in()."""

        return self.filter_in(column, operator, criteria)

    def filter_out(self, column: str, operator: str, criteria: str):
        self.session.params[column] = f"not.{operator}.{criteria}"
        return self

    def not_(self, column: str, operator: str, criteria: str):
        """Alias to Self.filter_out()."""

        return self.filter_out(column, operator, criteria)

    def eq(self, column: str, criteria: str):
        return self.filter_in(column, "eq", criteria)

    def neq(self, column: str, criteria: str):
        return self.filter_in(column, "neq", criteria)

    def gt(self, column: str, criteria: str):
        return self.filter_in(column, "gt", criteria)

    def lt(self, column: str, criteria: str):
        return self.filter_in(column, "lt", criteria)

    def gte(self, column: str, criteria: str):
        return self.filter_in(column, "gte", criteria)

    def lte(self, column: str, criteria: str):
        return self.filter_in(column, "lte", criteria)

    def like(self, column: str, criteria: str):
        return self.filter_in(column, "like", criteria)

    def ilike(self, column: str, criteria: str):
        return self.filter_in(column, "ilike", criteria)

    def is_(self, column: str, criteria: str):
        return self.filter_in(column, "is", criteria)

    def in_(self, column: str, criteria: str):
        return self.filter_in(column, "in", criteria)

    def fts(self, column: str, criteria: str):
        return self.filter_in(column, "fts", criteria)

    def plfts(self, column: str, criteria: str):
        return self.filter_in(column, "plfts", criteria)

    def phfts(self, column: str, criteria: str):
        return self.filter_in(column, "phfts", criteria)

    def wfts(self, column: str, criteria: str):
        return self.filter_in(column, "wfts", criteria)

    def cs(self, column: str, criteria: str):
        return self.filter_in(column, "cs", criteria)

    def cd(self, column: str, criteria: str):
        return self.filter_in(column, "cd", criteria)

    def ova(self, column: str, criteria: str):
        return self.filter_in(column, "ova", criteria)

    def ovr(self, column: str, criteria: str):
        return self.filter_in(column, "ovr", criteria)

    def sl(self, column: str, criteria: str):
        return self.filter_in(column, "sl", criteria)

    def sr(self, column: str, criteria: str):
        return self.filter_in(column, "sr", criteria)

    def nxr(self, column: str, criteria: str):
        return self.filter_in(column, "nxr", criteria)

    def nxl(self, column: str, criteria: str):
        return self.filter_in(column, "nxl", criteria)

    def adj(self, column: str, criteria: str):
        return self.filter_in(column, "adj", criteria)

    # def or_(self, column: str, criteria: str):
    #     return self.filter_in(column, "or", criteria)


class GetRequestBuilder(RequestBuilder):
    @classmethod
    def from_request_builder(cls, builder: RequestBuilder):
        result = cls(builder.session, builder.path)
        result.json = builder.json
        result.http_method = builder.http_method
        return result

    def order(self, column: str, *, desc=False, nullsfirst=False):
        self.session.params[
            "order"
        ] = f"{column}{'.desc' if desc else ''}{'.nullsfirst' if nullsfirst else ''}"
        return self

    def limit(self, size: int, *, start=0):
        self.session.headers["Range-Unit"] = "items"
        self.session.headers["Range"] = f"{start}-{start + size - 1}"
        return self

    def range(self, start: int, end: int):
        self.session.headers["Range-Unit"] = "items"
        self.session.headers["Range"] = f"{start}-{end - 1}"
        return self

    def single(self):
        self.session.headers["Accept"] = "application/vnd.pgrst.object+json"
        return self

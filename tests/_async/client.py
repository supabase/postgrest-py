from postgrest import AsyncPostgrestClient

REST_URL = "http://127.0.0.1:3000"


def rest_client():
    return AsyncPostgrestClient(
        base_url=REST_URL,
    )

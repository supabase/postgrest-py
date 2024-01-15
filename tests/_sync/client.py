from postgrest import SyncPostgrestClient

REST_URL = "http://127.0.0.1:3000"


def rest_client():
    return SyncPostgrestClient(
        base_url=REST_URL,
    )

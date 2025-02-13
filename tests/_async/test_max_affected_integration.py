import pytest

from postgrest.exceptions import APIError
from postgrest.types import Handling

from .client import rest_client


async def test_update_more_rows_that_should_be_affected():
    with pytest.raises(
        APIError, match="Query result exceeds max-affected preference constraint"
    ):
        (
            await rest_client()
            .from_("countries")
            .update(
                {"country_name": "COUNTRY_NAME_CHANGED"},
                handling=Handling.strict,
                max_affected=1,
            )
            .in_("nicename", ["Albania", "Algeria"])
            .execute()
        )


async def test_delete_more_rows_that_should_be_affected():
    with pytest.raises(
        APIError, match="Query result exceeds max-affected preference constraint"
    ):
        (
            await rest_client()
            .from_("countries")
            .delete(handling=Handling.strict, max_affected=1)
            .in_("nicename", ["Albania", "Algeria"])
            .execute()
        )

from .client import rest_client


def test_multivalued_param():
    res = (
        rest_client()
        .from_("countries")
        .select("country_name, iso", count="exact")
        .lte("numcode", 8)
        .gte("numcode", 4)
        .execute()
    )

    assert res.count == 2
    assert res.data == [
        {"country_name": "AFGHANISTAN", "iso": "AF"},
        {"country_name": "ALBANIA", "iso": "AL"},
    ]


def test_match():
    res = (
        rest_client()
        .from_("countries")
        .select("country_name, iso")
        .match({"numcode": 8, "nicename": "Albania"})
        .single()
        .execute()
    )

    assert res.data == {"country_name": "ALBANIA", "iso": "AL"}


def test_equals():
    res = (
        rest_client()
        .from_("countries")
        .select("country_name, iso")
        .eq("nicename", "Albania")
        .single()
        .execute()
    )

    assert res.data == {"country_name": "ALBANIA", "iso": "AL"}


def test_not_equal():
    res = (
        rest_client()
        .from_("users")
        .select("id, name")
        .neq("name", "Jane")
        .single()
        .execute()
    )

    assert res.data == {"id": 1, "name": "Michael"}


def test_greater_than():
    res = rest_client().from_("users").select("id, name").gt("id", 1).single().execute()

    assert res.data == {"id": 2, "name": "Jane"}


def test_greater_than_or_equals_to():
    res = rest_client().from_("users").select("id, name").gte("id", 1).execute()

    assert res.data == [{"id": 1, "name": "Michael"}, {"id": 2, "name": "Jane"}]


def test_contains_dictionary():
    res = (
        rest_client()
        .from_("users")
        .select("name")
        .contains("address", {"postcode": 90210})
        .single()
        .execute()
    )

    assert res.data == {"name": "Michael"}


def test_contains_any_item():
    res = (
        rest_client()
        .from_("issues")
        .select("title")
        .contains("tags", ["is:open", "priority:low"])
        .execute()
    )

    assert res.data == [{"title": "Cache invalidation is not working"}]


def test_contains_on_range():
    res = (
        rest_client()
        .from_("reservations")
        .select("id, room_name")
        .contains("during", "[2000-01-01 13:00, 2000-01-01 13:30)")
        .execute()
    )

    assert res.data == [{"id": 1, "room_name": "Emerald"}]


def test_contained_by_mixed_items():
    res = (
        rest_client()
        .from_("reservations")
        .select("id, room_name")
        .contained_by("during", "[2000-01-01 00:00, 2000-01-01 23:59)")
        .execute()
    )

    assert res.data == [{"id": 1, "room_name": "Emerald"}]


def test_range_greater_than():
    res = (
        rest_client()
        .from_("reservations")
        .select("id, room_name")
        .range_gt("during", ["2000-01-02 08:00", "2000-01-02 09:00"])
        .execute()
    )

    assert res.data == [{"id": 2, "room_name": "Topaz"}]


def test_range_greater_than_or_equal_to():
    res = (
        rest_client()
        .from_("reservations")
        .select("id, room_name")
        .range_gte("during", ["2000-01-02 08:30", "2000-01-02 09:30"])
        .execute()
    )

    assert res.data == [{"id": 2, "room_name": "Topaz"}]


def test_range_less_than():
    res = (
        rest_client()
        .from_("reservations")
        .select("id, room_name")
        .range_lt("during", ["2000-01-01 15:00", "2000-01-02 16:00"])
        .execute()
    )

    assert res.data == [{"id": 1, "room_name": "Emerald"}]


def test_range_less_than_or_equal_to():
    res = (
        rest_client()
        .from_("reservations")
        .select("id, room_name")
        .range_lte("during", ["2000-01-01 14:00", "2000-01-01 16:00"])
        .execute()
    )

    assert res.data == [{"id": 1, "room_name": "Emerald"}]


def test_range_adjacent():
    res = (
        rest_client()
        .from_("reservations")
        .select("id, room_name")
        .range_adjacent("during", ["2000-01-01 12:00", "2000-01-01 13:00"])
        .execute()
    )

    assert res.data == [{"id": 1, "room_name": "Emerald"}]


def test_overlaps():
    res = (
        rest_client()
        .from_("issues")
        .select("title")
        .overlaps("tags", ["is:closed", "severity:high"])
        .execute()
    )

    assert res.data == [
        {"title": "Cache invalidation is not working"},
        {"title": "Add alias to filters"},
    ]


def test_like():
    res = (
        rest_client()
        .from_("countries")
        .select("country_name, iso")
        .like("nicename", "%Alba%")
        .execute()
    )

    assert res.data == [{"country_name": "ALBANIA", "iso": "AL"}]


def test_ilike():
    res = (
        rest_client()
        .from_("countries")
        .select("country_name, iso")
        .ilike("nicename", "%alban%")
        .execute()
    )

    assert res.data == [{"country_name": "ALBANIA", "iso": "AL"}]


def test_is_():
    res = (
        rest_client()
        .from_("countries")
        .select("country_name, iso")
        .is_("numcode", "null")
        .limit(1)
        .order("nicename")
        .execute()
    )

    assert res.data == [{"country_name": "ANTARCTICA", "iso": "AQ"}]


def test_is_not():
    res = (
        rest_client()
        .from_("countries")
        .select("country_name, iso")
        .not_.is_("numcode", "null")
        .limit(1)
        .order("nicename")
        .execute()
    )

    assert res.data == [{"country_name": "AFGHANISTAN", "iso": "AF"}]


def test_in_():
    res = (
        rest_client()
        .from_("countries")
        .select("country_name, iso")
        .in_("nicename", ["Albania", "Algeria"])
        .execute()
    )

    assert res.data == [
        {"country_name": "ALBANIA", "iso": "AL"},
        {"country_name": "ALGERIA", "iso": "DZ"},
    ]


def test_or_():
    res = (
        rest_client()
        .from_("countries")
        .select("country_name, iso")
        .or_("iso.eq.DZ,nicename.eq.Albania")
        .execute()
    )

    assert res.data == [
        {"country_name": "ALBANIA", "iso": "AL"},
        {"country_name": "ALGERIA", "iso": "DZ"},
    ]


def test_or_with_and():
    res = (
        rest_client()
        .from_("countries")
        .select("country_name, iso")
        .or_("phonecode.gt.506,and(iso.eq.AL,nicename.eq.Albania)")
        .execute()
    )

    assert res.data == [
        {"country_name": "ALBANIA", "iso": "AL"},
        {"country_name": "TRINIDAD AND TOBAGO", "iso": "TT"},
    ]


def test_or_in():
    res = (
        rest_client()
        .from_("issues")
        .select("id, title")
        .or_("id.in.(1,4),tags.cs.{is:open,priority:high}")
        .execute()
    )

    assert res.data == [
        {"id": 1, "title": "Cache invalidation is not working"},
        {"id": 3, "title": "Add missing postgrest filters"},
        {"id": 4, "title": "Add alias to filters"},
    ]


def test_or_on_reference_table():
    res = (
        rest_client()
        .from_("countries")
        .select("country_name, cities!inner(name)")
        .or_("country_id.eq.10,name.eq.Paris", reference_table="cities")
        .execute()
    )

    assert res.data == [
        {
            "country_name": "UNITED KINGDOM",
            "cities": [
                {"name": "London"},
                {"name": "Manchester"},
                {"name": "Liverpool"},
                {"name": "Bristol"},
            ],
        },
    ]

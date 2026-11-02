from app.cities import get_default_cities


def test_default_cities_has_ten_entries() -> None:
    cities = get_default_cities()
    assert len(cities) == 10


def test_default_cities_include_required_fields() -> None:
    cities = get_default_cities()
    names = {city["City"] for city in cities}
    assert "New York" in names
    assert "Tokyo" in names
    assert "Rio de Janeiro" in names
    for city in cities:
        assert "Latitude" in city
        assert "Longitude" in city


def test_get_default_cities_returns_copy() -> None:
    first = get_default_cities()
    first[0]["City"] = "Changed"
    second = get_default_cities()
    assert second[0]["City"] == "New York"

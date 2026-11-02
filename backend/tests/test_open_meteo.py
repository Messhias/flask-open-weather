"""Open-Meteo client tests using mocked HTTP responses shaped like the real API.

Docs: https://open-meteo.com/en/docs
- Multiple coordinates: comma-separated latitude/longitude
- Multi-location JSON becomes a list of structures
- current=temperature_2m,relative_humidity_2m,wind_speed_10m
- wind_speed_unit=ms, temperature_unit=celsius
"""

import httpx
import pytest
import respx

from app.cities import City
from app.open_meteo import (
    CURRENT_VARS,
    OPEN_METEO_URL,
    OpenMeteoClient,
    WeatherUpstreamError,
)


def _current_payload(
    *,
    temperature: float,
    humidity: float,
    wind_ms: float,
    latitude: float,
    longitude: float,
) -> dict:
    """Build a payload matching Open-Meteo current-weather response shape."""
    return {
        "latitude": latitude,
        "longitude": longitude,
        "generationtime_ms": 0.05,
        "utc_offset_seconds": 0,
        "timezone": "GMT",
        "timezone_abbreviation": "GMT",
        "elevation": 32.0,
        "current_units": {
            "time": "iso8601",
            "interval": "seconds",
            "temperature_2m": "°C",
            "relative_humidity_2m": "%",
            "wind_speed_10m": "m/s",
        },
        "current": {
            "time": "2026-11-02T17:00",
            "interval": 900,
            "temperature_2m": temperature,
            "relative_humidity_2m": humidity,
            "wind_speed_10m": wind_ms,
        },
    }


@respx.mock
def test_fetch_current_batches_cities_in_one_request_with_doc_params() -> None:
    cities: list[City] = [
        {"City": "New York", "Latitude": 40.7128, "Longitude": -74.0060},
        {"City": "Tokyo", "Latitude": 35.6895, "Longitude": 139.6917},
    ]
    route = respx.get(OPEN_METEO_URL).mock(
        return_value=httpx.Response(
            200,
            json=[
                _current_payload(
                    temperature=17.3,
                    humidity=40,
                    wind_ms=3.72,
                    latitude=40.71,
                    longitude=-73.99,
                ),
                _current_payload(
                    temperature=14.1,
                    humidity=62,
                    wind_ms=2.4,
                    latitude=35.69,
                    longitude=139.69,
                ),
            ],
        )
    )

    client = OpenMeteoClient(max_retries=0)
    rows = client.fetch_current(cities)
    client.close()

    assert route.call_count == 1
    request = route.calls[0].request
    assert request.url.params["latitude"] == "40.7128,35.6895"
    assert request.url.params["longitude"] == "-74.006,139.6917"
    assert request.url.params["current"] == CURRENT_VARS
    assert request.url.params["wind_speed_unit"] == "ms"
    assert request.url.params["temperature_unit"] == "celsius"
    assert rows == [
        {
            "City": "New York",
            "temperature_c": 17.3,
            "humidity": 40,
            "wind_speed_ms": 3.72,
        },
        {
            "City": "Tokyo",
            "temperature_c": 14.1,
            "humidity": 62,
            "wind_speed_ms": 2.4,
        },
    ]


@respx.mock
def test_fetch_current_supports_single_city_object_response() -> None:
    city: City = {"City": "Berlin", "Latitude": 52.52, "Longitude": 13.405}
    respx.get(OPEN_METEO_URL).mock(
        return_value=httpx.Response(
            200,
            json=_current_payload(
                temperature=12.5,
                humidity=70,
                wind_ms=3.2,
                latitude=52.52,
                longitude=13.41,
            ),
        )
    )

    client = OpenMeteoClient(max_retries=0)
    rows = client.fetch_current([city])
    client.close()

    assert rows == [
        {
            "City": "Berlin",
            "temperature_c": 12.5,
            "humidity": 70,
            "wind_speed_ms": 3.2,
        }
    ]


@respx.mock
def test_fetch_current_retries_on_503_then_succeeds() -> None:
    city: City = {"City": "Berlin", "Latitude": 52.52, "Longitude": 13.405}
    route = respx.get(OPEN_METEO_URL).mock(
        side_effect=[
            httpx.Response(503, json={"error": True, "reason": "Service Unavailable"}),
            httpx.Response(
                200,
                json=_current_payload(
                    temperature=12.5,
                    humidity=70,
                    wind_ms=3.2,
                    latitude=52.52,
                    longitude=13.41,
                ),
            ),
        ]
    )

    client = OpenMeteoClient(max_retries=2, retry_backoff_seconds=0)
    rows = client.fetch_current([city])
    client.close()

    assert route.call_count == 2
    assert rows[0]["City"] == "Berlin"


@respx.mock
def test_fetch_current_raises_upstream_error_after_retries() -> None:
    city: City = {"City": "Berlin", "Latitude": 52.52, "Longitude": 13.405}
    respx.get(OPEN_METEO_URL).mock(
        return_value=httpx.Response(503, json={"error": True, "reason": "Service Unavailable"})
    )

    client = OpenMeteoClient(max_retries=1, retry_backoff_seconds=0)
    with pytest.raises(WeatherUpstreamError, match="HTTP 503"):
        client.fetch_current([city])
    client.close()


@respx.mock
def test_fetch_current_raises_when_location_count_mismatches() -> None:
    cities: list[City] = [
        {"City": "Berlin", "Latitude": 52.52, "Longitude": 13.405},
        {"City": "Paris", "Latitude": 48.8566, "Longitude": 2.3522},
    ]
    respx.get(OPEN_METEO_URL).mock(
        return_value=httpx.Response(
            200,
            json=_current_payload(
                temperature=12.5,
                humidity=70,
                wind_ms=3.2,
                latitude=52.52,
                longitude=13.41,
            ),
        )
    )

    client = OpenMeteoClient(max_retries=0)
    with pytest.raises(WeatherUpstreamError, match="locations"):
        client.fetch_current(cities)
    client.close()

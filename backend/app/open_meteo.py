"""Open-Meteo HTTP client for current weather conditions."""

from __future__ import annotations

from typing import Protocol

import httpx

from app.cities import City

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
CURRENT_VARS = "temperature_2m,relative_humidity_2m,wind_speed_10m"


class WeatherClient(Protocol):
    def fetch_current(self, cities: list[City]) -> list[dict]:
        """Fetch current weather rows for the given cities."""


class OpenMeteoClient:
    """Fetch current weather from the public Open-Meteo forecast API."""

    def __init__(self, client: httpx.Client | None = None) -> None:
        self._client = client
        self._owns_client = client is None

    def _get_client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(timeout=30.0)
        return self._client

    def close(self) -> None:
        if self._owns_client and self._client is not None:
            self._client.close()
            self._client = None

    def fetch_current(self, cities: list[City]) -> list[dict]:
        """Return raw weather rows keyed for processing.build_weather_dataframe."""
        results: list[dict] = []
        client = self._get_client()
        for city in cities:
            response = client.get(
                OPEN_METEO_URL,
                params={
                    "latitude": city["Latitude"],
                    "longitude": city["Longitude"],
                    "current": CURRENT_VARS,
                    "wind_speed_unit": "ms",
                    "temperature_unit": "celsius",
                },
            )
            response.raise_for_status()
            payload = response.json()
            current = payload["current"]
            results.append(
                {
                    "City": city["City"],
                    "temperature_c": current["temperature_2m"],
                    "humidity": current["relative_humidity_2m"],
                    "wind_speed_ms": current["wind_speed_10m"],
                }
            )
        return results

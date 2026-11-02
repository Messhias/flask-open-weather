"""Open-Meteo HTTP client for current weather conditions."""

from __future__ import annotations

import time
from typing import Any, Protocol

import httpx

from app.cities import City

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
CURRENT_VARS = "temperature_2m,relative_humidity_2m,wind_speed_10m"
RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class WeatherUpstreamError(RuntimeError):
    """Raised when Open-Meteo cannot be reached successfully."""


class WeatherClient(Protocol):
    def fetch_current(self, cities: list[City]) -> list[dict]:
        """Fetch current weather rows for the given cities."""


class OpenMeteoClient:
    """Fetch current weather from the public Open-Meteo forecast API."""

    def __init__(
        self,
        client: httpx.Client | None = None,
        *,
        max_retries: int = 3,
        retry_backoff_seconds: float = 0.8,
    ) -> None:
        self._client = client
        self._owns_client = client is None
        self._max_retries = max_retries
        self._retry_backoff_seconds = retry_backoff_seconds

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
        if not cities:
            return []

        client = self._get_client()
        params = {
            "latitude": ",".join(str(city["Latitude"]) for city in cities),
            "longitude": ",".join(str(city["Longitude"]) for city in cities),
            "current": CURRENT_VARS,
            "wind_speed_unit": "ms",
            "temperature_unit": "celsius",
        }
        payload = self._request_json(client, params)
        return self._parse_payload(cities, payload)

    def _request_json(self, client: httpx.Client, params: dict[str, str]) -> Any:
        last_error: Exception | None = None
        for attempt in range(self._max_retries + 1):
            try:
                response = client.get(OPEN_METEO_URL, params=params)
                if response.status_code in RETRYABLE_STATUS and attempt < self._max_retries:
                    time.sleep(self._retry_backoff_seconds * (attempt + 1))
                    continue
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as exc:
                last_error = exc
                if (
                    exc.response.status_code in RETRYABLE_STATUS
                    and attempt < self._max_retries
                ):
                    time.sleep(self._retry_backoff_seconds * (attempt + 1))
                    continue
                raise WeatherUpstreamError(
                    f"Open-Meteo returned HTTP {exc.response.status_code}"
                ) from exc
            except httpx.HTTPError as exc:
                last_error = exc
                if attempt < self._max_retries:
                    time.sleep(self._retry_backoff_seconds * (attempt + 1))
                    continue
                raise WeatherUpstreamError("Open-Meteo request failed") from exc

        raise WeatherUpstreamError("Open-Meteo request failed") from last_error

    @staticmethod
    def _parse_payload(cities: list[City], payload: Any) -> list[dict]:
        entries = payload if isinstance(payload, list) else [payload]
        if len(entries) != len(cities):
            raise WeatherUpstreamError(
                f"Open-Meteo returned {len(entries)} locations for {len(cities)} cities"
            )

        results: list[dict] = []
        for city, entry in zip(cities, entries, strict=True):
            current = entry["current"]
            results.append(
                {
                    "City": city["City"],
                    "temperature_c": current["temperature_2m"],
                    "humidity": current["relative_humidity_2m"],
                    "wind_speed_ms": current["wind_speed_10m"],
                }
            )
        return results

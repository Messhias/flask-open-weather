from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app, set_service
from app.open_meteo import WeatherUpstreamError
from app.service import WeatherService


class FakeClient:
    def fetch_current(self, cities):
        return [
            {
                "City": city["City"],
                "temperature_c": 20 + index,
                "humidity": 40 + index,
                "wind_speed_ms": 2 + index * 0.1,
            }
            for index, city in enumerate(cities)
        ]


class FailingClient:
    def fetch_current(self, cities):
        raise WeatherUpstreamError("Open-Meteo returned HTTP 503")


def _client(tmp_path: Path) -> TestClient:
    service = WeatherService(client=FakeClient(), data_dir=tmp_path)
    set_service(service)
    return TestClient(app)


def test_health() -> None:
    set_service(WeatherService(client=FakeClient(), data_dir="data"))
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_weather(tmp_path: Path) -> None:
    client = _client(tmp_path)
    response = client.get("/api/weather")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload["rows"]) == 10
    assert "Temperature (C)" in payload["rows"][0]


def test_download_csv(tmp_path: Path) -> None:
    client = _client(tmp_path)
    response = client.get("/api/weather/csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "City" in response.text


def test_temperature_chart(tmp_path: Path) -> None:
    client = _client(tmp_path)
    response = client.get("/api/charts/temperature")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert response.content.startswith(b"\x89PNG")


def test_refresh(tmp_path: Path) -> None:
    client = _client(tmp_path)
    response = client.post("/api/weather/refresh")
    assert response.status_code == 200
    assert response.json()["count"] == 10


def test_refresh_returns_502_on_upstream_failure(tmp_path: Path) -> None:
    set_service(WeatherService(client=FailingClient(), data_dir=tmp_path))
    client = TestClient(app)
    response = client.post("/api/weather/refresh")
    assert response.status_code == 502
    assert "Open-Meteo" in response.json()["detail"]

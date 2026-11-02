from pathlib import Path

from app.csv_export import export_weather_csv
from app.cli import main
from app.processing import build_weather_dataframe


def test_export_weather_csv(tmp_path: Path) -> None:
    df = build_weather_dataframe(
        [
            {
                "City": "London",
                "temperature_c": 15,
                "humidity": 60,
                "wind_speed_ms": 4,
            }
        ]
    )
    path = export_weather_csv(df, tmp_path / "weather_data.csv")
    content = path.read_text()
    assert "City,Temperature (C),Temperature (F),Humidity (%),Wind Speed (m/s),Wind Speed (mph)" in content
    assert "London" in content


def test_cli_writes_csv(tmp_path: Path, monkeypatch) -> None:
    class FakeClient:
        def fetch_current(self, cities):
            return [
                {
                    "City": city["City"],
                    "temperature_c": 10,
                    "humidity": 50,
                    "wind_speed_ms": 1,
                }
                for city in cities
            ]

    from app import service as service_module

    original = service_module.OpenMeteoClient
    monkeypatch.setattr(service_module, "OpenMeteoClient", lambda: FakeClient())

    output = tmp_path / "weather_data.csv"
    code = main(["--output", str(output), "--data-dir", str(tmp_path)])
    assert code == 0
    assert output.exists()
    assert output.read_text().count("\n") >= 11

    monkeypatch.setattr(service_module, "OpenMeteoClient", original)

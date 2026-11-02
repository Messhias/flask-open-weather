from app.charts import temperature_bar_chart_png
from app.processing import build_weather_dataframe


def test_temperature_bar_chart_png_is_non_empty_png() -> None:
    df = build_weather_dataframe(
        [
            {
                "City": "Tokyo",
                "temperature_c": 18,
                "humidity": 65,
                "wind_speed_ms": 2.5,
            },
            {
                "City": "Paris",
                "temperature_c": 14,
                "humidity": 70,
                "wind_speed_ms": 3.1,
            },
        ]
    )
    png = temperature_bar_chart_png(df)
    assert png.startswith(b"\x89PNG")
    assert len(png) > 100

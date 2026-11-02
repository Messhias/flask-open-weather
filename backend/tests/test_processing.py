import pandas as pd

from app.processing import (
    build_weather_dataframe,
    celsius_to_fahrenheit,
    meters_per_second_to_mph,
    rank_by_humidity,
    rank_by_temperature,
)


def test_celsius_to_fahrenheit() -> None:
    assert celsius_to_fahrenheit(0) == 32
    assert celsius_to_fahrenheit(100) == 212
    assert celsius_to_fahrenheit(25) == 77


def test_meters_per_second_to_mph() -> None:
    assert round(meters_per_second_to_mph(1), 4) == 2.2369


def test_build_weather_dataframe_columns_and_conversions() -> None:
    rows = [
        {
            "City": "Paris",
            "temperature_c": 20,
            "humidity": 55,
            "wind_speed_ms": 2,
        }
    ]
    df = build_weather_dataframe(rows)
    assert list(df.columns) == [
        "City",
        "Temperature (C)",
        "Temperature (F)",
        "Humidity (%)",
        "Wind Speed (m/s)",
        "Wind Speed (mph)",
    ]
    assert df.iloc[0]["Temperature (F)"] == 68.0
    assert df.iloc[0]["Wind Speed (mph)"] == round(2 * 2.2369362921, 2)


def test_rank_by_temperature_highest_first() -> None:
    df = pd.DataFrame(
        {
            "City": ["A", "B"],
            "Temperature (C)": [10, 30],
            "Temperature (F)": [50, 86],
            "Humidity (%)": [80, 40],
            "Wind Speed (m/s)": [1, 2],
            "Wind Speed (mph)": [2.24, 4.47],
        }
    )
    ranked = rank_by_temperature(df)
    assert ranked.iloc[0]["City"] == "B"


def test_rank_by_humidity_lowest_first() -> None:
    df = pd.DataFrame(
        {
            "City": ["A", "B"],
            "Temperature (C)": [10, 30],
            "Temperature (F)": [50, 86],
            "Humidity (%)": [80, 40],
            "Wind Speed (m/s)": [1, 2],
            "Wind Speed (mph)": [2.24, 4.47],
        }
    )
    ranked = rank_by_humidity(df)
    assert ranked.iloc[0]["City"] == "B"

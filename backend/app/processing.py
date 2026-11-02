"""Weather data conversions, DataFrame construction, and ranking helpers."""

from __future__ import annotations

from typing import Any

import pandas as pd

CSV_COLUMNS = [
    "City",
    "Temperature (C)",
    "Temperature (F)",
    "Humidity (%)",
    "Wind Speed (m/s)",
    "Wind Speed (mph)",
]


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def meters_per_second_to_mph(meters_per_second: float) -> float:
    """Convert meters per second to miles per hour."""
    return meters_per_second * 2.2369362921


def build_weather_dataframe(rows: list[dict[str, Any]]) -> pd.DataFrame:
    """
    Build a weather DataFrame with converted units.

    Expected input keys per row:
    City, temperature_c, humidity, wind_speed_ms
    """
    records: list[dict[str, Any]] = []
    for row in rows:
        temp_c = float(row["temperature_c"])
        wind_ms = float(row["wind_speed_ms"])
        records.append(
            {
                "City": row["City"],
                "Temperature (C)": round(temp_c, 2),
                "Temperature (F)": round(celsius_to_fahrenheit(temp_c), 2),
                "Humidity (%)": round(float(row["humidity"]), 2),
                "Wind Speed (m/s)": round(wind_ms, 2),
                "Wind Speed (mph)": round(meters_per_second_to_mph(wind_ms), 2),
            }
        )
    return pd.DataFrame(records, columns=CSV_COLUMNS)


def rank_by_temperature(df: pd.DataFrame, *, ascending: bool = False) -> pd.DataFrame:
    """Rank cities by temperature in Celsius."""
    return df.sort_values("Temperature (C)", ascending=ascending).reset_index(drop=True)


def rank_by_humidity(df: pd.DataFrame, *, ascending: bool = True) -> pd.DataFrame:
    """Rank cities by humidity (default: lowest first)."""
    return df.sort_values("Humidity (%)", ascending=ascending).reset_index(drop=True)

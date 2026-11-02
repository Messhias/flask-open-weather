"""Application service orchestrating fetch, process, export, and charts."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.cities import City, get_default_cities
from app.charts import temperature_bar_chart_png
from app.csv_export import export_weather_csv
from app.open_meteo import OpenMeteoClient, WeatherClient
from app.processing import build_weather_dataframe, rank_by_humidity, rank_by_temperature


class WeatherService:
    def __init__(
        self,
        client: WeatherClient | None = None,
        data_dir: str | Path = "data",
    ) -> None:
        self._client = client or OpenMeteoClient()
        self._data_dir = Path(data_dir)
        self._df: pd.DataFrame | None = None

    @property
    def dataframe(self) -> pd.DataFrame:
        if self._df is None:
            self.refresh()
        assert self._df is not None
        return self._df

    def refresh(self, cities: list[City] | None = None) -> pd.DataFrame:
        selected = cities or get_default_cities()
        rows = self._client.fetch_current(selected)
        self._df = build_weather_dataframe(rows)
        export_weather_csv(self._df, self.csv_path)
        return self._df

    @property
    def csv_path(self) -> Path:
        return self._data_dir / "weather_data.csv"

    def ranked(
        self,
        *,
        by: str = "temperature",
        ascending: bool | None = None,
    ) -> pd.DataFrame:
        df = self.dataframe
        if by == "humidity":
            return rank_by_humidity(
                df,
                ascending=True if ascending is None else ascending,
            )
        return rank_by_temperature(
            df,
            ascending=False if ascending is None else ascending,
        )

    def temperature_chart_png(self) -> bytes:
        return temperature_bar_chart_png(self.dataframe)

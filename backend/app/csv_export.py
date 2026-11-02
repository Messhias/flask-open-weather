"""CSV export helpers for processed weather data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.processing import CSV_COLUMNS


def export_weather_csv(df: pd.DataFrame, path: str | Path) -> Path:
    """Write the weather DataFrame to CSV with the exercise column order."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    ordered = df.loc[:, CSV_COLUMNS]
    ordered.to_csv(output, index=False)
    return output

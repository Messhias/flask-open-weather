"""Matplotlib chart generation for weather summaries."""

from __future__ import annotations

import io

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402


def temperature_bar_chart_png(df: pd.DataFrame) -> bytes:
    """Render a temperature bar chart and return PNG bytes."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df["City"], df["Temperature (C)"], color="#0e7490")
    ax.set_title("Current Temperature by City")
    ax.set_ylabel("Temperature (C)")
    ax.set_xlabel("City")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    plt.close(fig)
    buffer.seek(0)
    return buffer.read()

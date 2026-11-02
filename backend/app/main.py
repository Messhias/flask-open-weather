"""FastAPI application exposing weather JSON, CSV, and chart endpoints."""

from __future__ import annotations

import os
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response

from app.cities import get_default_cities
from app.open_meteo import WeatherUpstreamError
from app.service import WeatherService

app = FastAPI(title="Weather Data API", version="0.1.0")

_cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:8080,http://localhost:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_service: WeatherService | None = None


def get_service() -> WeatherService:
    global _service
    if _service is None:
        data_dir = os.getenv("WEATHER_DATA_DIR", "data")
        _service = WeatherService(data_dir=data_dir)
    return _service


def set_service(service: WeatherService) -> None:
    """Test helper to inject a WeatherService instance."""
    global _service
    _service = service


ServiceDep = Annotated[WeatherService, Depends(get_service)]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def _run_weather(callback):
    try:
        return callback()
    except WeatherUpstreamError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.get("/api/weather")
def get_weather(
    service: ServiceDep,
    sort_by: Annotated[str, Query()] = "temperature",
    ascending: Annotated[bool | None, Query()] = None,
) -> dict:
    df = _run_weather(lambda: service.ranked(by=sort_by, ascending=ascending))
    return {
        "cities": get_default_cities(),
        "rows": df.to_dict(orient="records"),
    }


@app.get("/api/weather/csv")
def download_csv(service: ServiceDep) -> FileResponse:
    _run_weather(lambda: service.dataframe)
    return FileResponse(
        path=service.csv_path,
        media_type="text/csv",
        filename="weather_data.csv",
    )


@app.get("/api/charts/temperature")
def temperature_chart(service: ServiceDep) -> Response:
    png = _run_weather(service.temperature_chart_png)
    return Response(content=png, media_type="image/png")


@app.post("/api/weather/refresh")
def refresh_weather(service: ServiceDep) -> dict:
    df = _run_weather(service.refresh)
    return {"count": len(df), "rows": df.to_dict(orient="records")}

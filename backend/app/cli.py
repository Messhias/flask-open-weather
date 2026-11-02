"""CLI entrypoint for the weather scraping exercise."""

from __future__ import annotations

import argparse
from pathlib import Path

from app.cities import get_default_cities
from app.service import WeatherService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch Open-Meteo weather data and export weather_data.csv",
    )
    parser.add_argument(
        "--output",
        default="weather_data.csv",
        help="Output CSV path (default: weather_data.csv)",
    )
    parser.add_argument(
        "--data-dir",
        default=".",
        help="Directory used by the weather service for artifacts",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    service = WeatherService(data_dir=args.data_dir)
    df = service.refresh(get_default_cities())

    output = Path(args.output)
    if output.parent != Path("."):
        output.parent.mkdir(parents=True, exist_ok=True)
    # Prefer explicit --output path for the exercise deliverable.
    from app.csv_export import export_weather_csv

    export_weather_csv(df, output)
    print(f"Wrote {output.resolve()} with {len(df)} cities")
    print(df.to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

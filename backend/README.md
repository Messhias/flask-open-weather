# Weather API

FastAPI backend for the weather scraping exercise.

Full setup, Docker, CLI, and test instructions live in the [root README](../README.md).

```bash
uv sync --group dev
uv run uvicorn app.main:app --reload --port 8000
uv run pytest
uv run python -m app --output weather_data.csv
```

# Weather Data Scraping

Monorepo for the IQ Weather Data Scraping exercise. The stack fetches current weather from [Open-Meteo](https://open-meteo.com/en/docs), processes it with pandas, exports `weather_data.csv`, serves charts and JSON through FastAPI, and shows a React dashboard.

## Stack

- Backend: Python 3.13, FastAPI, httpx, pandas, matplotlib, pytest
- Frontend: Vite 8, React 19, TypeScript, Tailwind CSS 4, Vitest
- Runtime: Docker Compose
- CI: GitHub Actions (pytest + Vitest on every push/PR)

## Quick start with Docker

```bash
docker compose up --build
```

- Web UI: http://localhost:8080
- API docs: http://localhost:8000/docs

## Local development

### Backend

```bash
cd backend
uv sync --group dev
uv run uvicorn app.main:app --reload --port 8000
```

CLI export (exercise deliverable):

```bash
cd backend
uv run python -m app --output weather_data.csv
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_URL=http://localhost:8000` if the UI is not using the Vite proxy.

## Tests

```bash
# Backend
cd backend && uv run pytest

# Frontend
cd frontend && npm test
```

CI runs the same suites on GitHub Actions.

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/weather` | Processed weather JSON (optional `sort_by`, `ascending`) |
| GET | `/api/weather/csv` | Download `weather_data.csv` |
| GET | `/api/charts/temperature` | Temperature bar chart PNG |
| POST | `/api/weather/refresh` | Refetch Open-Meteo data and regenerate artifacts |

## CSV columns

`City`, `Temperature (C)`, `Temperature (F)`, `Humidity (%)`, `Wind Speed (m/s)`, `Wind Speed (mph)`

## Interpreting the output

- Temperatures from Open-Meteo are Celsius; Fahrenheit is derived in pandas.
- Wind speeds are requested in `m/s` and also converted to mph.
- Rankings highlight the hottest city and the lowest humidity city.

## Repository

https://github.com/Messhias/flask-open-weather

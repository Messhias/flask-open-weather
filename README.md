# Weather Data Scraping

Monorepo for the IQ Weather Data Scraping exercise. The app fetches current weather from [Open-Meteo](https://open-meteo.com/en/docs), processes it with pandas, exports `weather_data.csv`, serves JSON/CSV/charts through FastAPI, and shows a React dashboard.

Repository: https://github.com/Messhias/flask-open-weather

## Prerequisites

Pick one path:

| Path | You need |
|------|----------|
| Docker (recommended) | Docker Desktop / Docker Engine + Compose v2 |
| Local backend | Python 3.13+ and [uv](https://docs.astral.sh/uv/) |
| Local frontend | Node.js 22+ and npm |

No Open-Meteo API key is required for the public forecast endpoint.

## Quick start (Docker)

```bash
git clone https://github.com/Messhias/flask-open-weather.git
cd flask-open-weather
docker compose up --build
```

Wait a few seconds for the API to become healthy, then open:

- Web UI: http://localhost:8080
- API Swagger: http://localhost:8000/docs
- Health: http://localhost:8000/health

Smoke test:

```bash
curl -sS http://localhost:8000/health
curl -sS -X POST http://localhost:8000/api/weather/refresh
curl -sS http://localhost:8000/api/weather | head
```

Stop:

```bash
docker compose down
```

## Local development

### Backend

```bash
cd backend
uv sync --group dev
uv run uvicorn app.main:app --reload --port 8000
```

CLI export (exercise CSV deliverable):

```bash
cd backend
uv run python -m app --output weather_data.csv
```

The CSV is written to the path you pass to `--output`.

### Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite serves http://localhost:5173 and proxies `/api` and `/health` to `http://localhost:8000`.

If you run the built frontend without that proxy, set:

```bash
export VITE_API_URL=http://localhost:8000
```

## Tests

Backend (pytest, Open-Meteo mocked with respx):

```bash
cd backend
uv run pytest
```

Frontend (Vitest + Testing Library):

```bash
cd frontend
npm test
```

Production frontend build check:

```bash
cd frontend
npm run build
```

CI runs backend and frontend tests on every push and pull request via GitHub Actions.

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/weather` | Processed weather JSON (`sort_by=temperature\|humidity`, optional `ascending`) |
| GET | `/api/weather/csv` | Download `weather_data.csv` |
| GET | `/api/charts/temperature` | Temperature bar chart PNG |
| POST | `/api/weather/refresh` | Refetch Open-Meteo data and regenerate artifacts |

### Upstream behavior

The client batches all cities into one Open-Meteo request (comma-separated latitudes/longitudes), retries transient `429`/`5xx` responses, and returns **HTTP 502** with a clear message if Open-Meteo stays unavailable.

## CSV columns

`City`, `Temperature (C)`, `Temperature (F)`, `Humidity (%)`, `Wind Speed (m/s)`, `Wind Speed (mph)`

## Interpreting the output

- Open-Meteo temperatures are requested in Celsius; Fahrenheit is derived in pandas.
- Wind speed is requested in `m/s` and also converted to mph.
- The dashboard ranks highest temperature and lowest humidity.

## Project layout

```text
backend/     FastAPI app, CLI, pytest suite
frontend/    Vite + React dashboard, Vitest suite
.github/     CI workflow
docker-compose.yml
```

## Troubleshooting

- `curl: (56) Connection reset`: the API container is still starting. Wait 2-5 seconds and retry `/health`.
- UI loads but data fails: confirm the API is up on port `8000` and check the browser network tab for `/api/weather`.
- Open-Meteo `503`: refresh again; the API retries automatically and surfaces a 502 only after retries are exhausted.

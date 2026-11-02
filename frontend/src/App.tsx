import { useCallback, useEffect, useState } from 'react'
import {
  csvDownloadUrl,
  fetchWeather,
  refreshWeather,
  temperatureChartUrl,
} from './api/weatherApi'
import { RankingPanel } from './components/RankingPanel'
import { WeatherTable } from './components/WeatherTable'
import type { WeatherRow } from './types'

function App() {
  const [rows, setRows] = useState<WeatherRow[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [chartKey, setChartKey] = useState(0)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await fetchWeather()
      setRows(data)
      setChartKey((value) => value + 1)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load weather')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void load()
  }, [load])

  async function handleRefresh() {
    setLoading(true)
    setError(null)
    try {
      const data = await refreshWeather()
      setRows(data)
      setChartKey((value) => value + 1)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to refresh weather')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-6xl flex-col gap-8 px-4 py-10">
      <header className="space-y-3">
        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-[var(--color-accent)]">
          Open-Meteo
        </p>
        <h1
          className="text-4xl font-semibold text-[var(--color-ink)]"
          style={{ fontFamily: 'var(--font-display)' }}
        >
          Weather Dashboard
        </h1>
        <p className="max-w-2xl text-[var(--color-muted)]">
          Current temperature, humidity, and wind for ten cities. Data is fetched
          from Open-Meteo, processed with pandas, and served by FastAPI.
        </p>
        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            onClick={() => void handleRefresh()}
            className="rounded-md bg-[var(--color-accent)] px-4 py-2 text-sm font-semibold text-white"
          >
            Refresh data
          </button>
          <a
            href={csvDownloadUrl()}
            className="rounded-md border border-[var(--color-border)] bg-white px-4 py-2 text-sm font-semibold text-[var(--color-ink)]"
          >
            Download CSV
          </a>
        </div>
      </header>

      {loading ? <p role="status">Loading weather data...</p> : null}
      {error ? (
        <p role="alert" className="text-red-700">
          {error}
        </p>
      ) : null}

      {!loading && !error ? (
        <>
          <RankingPanel rows={rows} />
          <WeatherTable rows={rows} />
          <section className="space-y-3">
            <h2 className="text-lg font-semibold">Temperature chart</h2>
            <img
              key={chartKey}
              src={`${temperatureChartUrl()}?t=${chartKey}`}
              alt="Bar chart of temperatures by city"
              className="w-full rounded-lg border border-[var(--color-border)] bg-white"
            />
          </section>
        </>
      ) : null}
    </main>
  )
}

export default App

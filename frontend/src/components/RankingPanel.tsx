import type { WeatherRow } from '../types'

type Props = {
  rows: WeatherRow[]
}

export function RankingPanel({ rows }: Props) {
  if (rows.length === 0) {
    return null
  }

  const hottest = [...rows].sort(
    (a, b) => b['Temperature (C)'] - a['Temperature (C)'],
  )[0]
  const driest = [...rows].sort(
    (a, b) => a['Humidity (%)'] - b['Humidity (%)'],
  )[0]

  return (
    <section aria-label="Rankings" className="grid gap-4 sm:grid-cols-2">
      <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-card)] p-4">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-[var(--color-muted)]">
          Highest temperature
        </h2>
        <p className="mt-2 text-xl font-semibold">
          {hottest.City} ({hottest['Temperature (C)']} C)
        </p>
      </div>
      <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-card)] p-4">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-[var(--color-muted)]">
          Lowest humidity
        </h2>
        <p className="mt-2 text-xl font-semibold">
          {driest.City} ({driest['Humidity (%)']}%)
        </p>
      </div>
    </section>
  )
}

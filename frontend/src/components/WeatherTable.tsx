import type { WeatherRow } from '../types'

type Props = {
  rows: WeatherRow[]
}

export function WeatherTable({ rows }: Props) {
  return (
    <div className="overflow-x-auto rounded-lg border border-[var(--color-border)] bg-[var(--color-card)]">
      <table className="min-w-full text-left text-sm">
        <caption className="sr-only">Current weather by city</caption>
        <thead className="bg-[var(--color-surface)] text-[var(--color-muted)]">
          <tr>
            <th className="px-4 py-3 font-semibold">City</th>
            <th className="px-4 py-3 font-semibold">Temp (C)</th>
            <th className="px-4 py-3 font-semibold">Temp (F)</th>
            <th className="px-4 py-3 font-semibold">Humidity (%)</th>
            <th className="px-4 py-3 font-semibold">Wind (m/s)</th>
            <th className="px-4 py-3 font-semibold">Wind (mph)</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.City} className="border-t border-[var(--color-border)]">
              <td className="px-4 py-3 font-medium">{row.City}</td>
              <td className="px-4 py-3">{row['Temperature (C)']}</td>
              <td className="px-4 py-3">{row['Temperature (F)']}</td>
              <td className="px-4 py-3">{row['Humidity (%)']}</td>
              <td className="px-4 py-3">{row['Wind Speed (m/s)']}</td>
              <td className="px-4 py-3">{row['Wind Speed (mph)']}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

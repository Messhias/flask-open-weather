import { afterEach, describe, expect, it, vi } from 'vitest'
import {
  csvDownloadUrl,
  fetchWeather,
  refreshWeather,
  temperatureChartUrl,
} from './weatherApi'

describe('weatherApi', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('fetchWeather maps API rows', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({
          rows: [{ City: 'London', 'Temperature (C)': 11 }],
        }),
      }),
    )

    const rows = await fetchWeather()
    expect(rows[0].City).toBe('London')
    expect(fetch).toHaveBeenCalledWith('/api/weather', undefined)
  })

  it('refreshWeather posts to refresh endpoint', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ rows: [] }),
      }),
    )

    await refreshWeather()
    expect(fetch).toHaveBeenCalledWith('/api/weather/refresh', {
      method: 'POST',
    })
  })

  it('builds download and chart urls', () => {
    expect(csvDownloadUrl()).toContain('/api/weather/csv')
    expect(temperatureChartUrl()).toContain('/api/charts/temperature')
  })
})

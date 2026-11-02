import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import App from './App'
import type { WeatherRow } from './types'

const sampleRows: WeatherRow[] = [
  {
    City: 'Berlin',
    'Temperature (C)': 12,
    'Temperature (F)': 53.6,
    'Humidity (%)': 70,
    'Wind Speed (m/s)': 3,
    'Wind Speed (mph)': 6.7,
  },
]

vi.mock('./api/weatherApi', () => ({
  fetchWeather: vi.fn(),
  refreshWeather: vi.fn(),
  csvDownloadUrl: () => '/api/weather/csv',
  temperatureChartUrl: () => '/api/charts/temperature',
}))

import { fetchWeather, refreshWeather } from './api/weatherApi'

describe('App', () => {
  beforeEach(() => {
    vi.mocked(fetchWeather).mockResolvedValue(sampleRows)
    vi.mocked(refreshWeather).mockResolvedValue([
      {
        ...sampleRows[0],
        'Temperature (C)': 15,
        'Temperature (F)': 59,
      },
    ])
  })

  it('loads weather table from the API', async () => {
    render(<App />)
    expect(await screen.findByText('Berlin')).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /download csv/i })).toHaveAttribute(
      'href',
      '/api/weather/csv',
    )
    expect(
      screen.getByRole('img', { name: /bar chart of temperatures/i }),
    ).toBeInTheDocument()
  })

  it('refreshes weather data when the button is clicked', async () => {
    const user = userEvent.setup()
    render(<App />)
    await screen.findByText('Berlin')
    await user.click(screen.getByRole('button', { name: /refresh data/i }))
    await waitFor(() => {
      expect(refreshWeather).toHaveBeenCalled()
    })
    expect(await screen.findByText('15')).toBeInTheDocument()
  })
})

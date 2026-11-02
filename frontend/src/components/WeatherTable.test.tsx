import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { WeatherTable } from './WeatherTable'
import type { WeatherRow } from '../types'

const rows: WeatherRow[] = [
  {
    City: 'Paris',
    'Temperature (C)': 18,
    'Temperature (F)': 64.4,
    'Humidity (%)': 55,
    'Wind Speed (m/s)': 2.1,
    'Wind Speed (mph)': 4.7,
  },
]

describe('WeatherTable', () => {
  it('renders city weather rows', () => {
    render(<WeatherTable rows={rows} />)
    expect(screen.getByText('Paris')).toBeInTheDocument()
    expect(screen.getByText('18')).toBeInTheDocument()
    expect(screen.getByText('55')).toBeInTheDocument()
  })
})

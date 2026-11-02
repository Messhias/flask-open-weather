import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { RankingPanel } from './RankingPanel'
import type { WeatherRow } from '../types'

const rows: WeatherRow[] = [
  {
    City: 'Cold City',
    'Temperature (C)': 5,
    'Temperature (F)': 41,
    'Humidity (%)': 90,
    'Wind Speed (m/s)': 1,
    'Wind Speed (mph)': 2.2,
  },
  {
    City: 'Hot City',
    'Temperature (C)': 30,
    'Temperature (F)': 86,
    'Humidity (%)': 20,
    'Wind Speed (m/s)': 3,
    'Wind Speed (mph)': 6.7,
  },
]

describe('RankingPanel', () => {
  it('shows hottest and driest cities', () => {
    render(<RankingPanel rows={rows} />)
    expect(screen.getByText(/Hot City \(30 C\)/)).toBeInTheDocument()
    expect(screen.getByText(/Hot City \(20%\)/)).toBeInTheDocument()
  })
})

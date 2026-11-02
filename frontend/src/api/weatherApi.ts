import type { WeatherResponse, WeatherRow } from '../types'

const API_BASE = import.meta.env.VITE_API_URL ?? ''

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, init)
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`)
  }
  return response.json() as Promise<T>
}

export async function fetchWeather(): Promise<WeatherRow[]> {
  const data = await request<WeatherResponse>('/api/weather')
  return data.rows
}

export async function refreshWeather(): Promise<WeatherRow[]> {
  const data = await request<{ rows: WeatherRow[] }>('/api/weather/refresh', {
    method: 'POST',
  })
  return data.rows
}

export function csvDownloadUrl(): string {
  return `${API_BASE}/api/weather/csv`
}

export function temperatureChartUrl(): string {
  return `${API_BASE}/api/charts/temperature`
}

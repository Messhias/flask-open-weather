export type WeatherRow = {
  City: string
  'Temperature (C)': number
  'Temperature (F)': number
  'Humidity (%)': number
  'Wind Speed (m/s)': number
  'Wind Speed (mph)': number
}

export type WeatherResponse = {
  rows: WeatherRow[]
}

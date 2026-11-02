import httpx
import respx

from app.cities import City
from app.open_meteo import OPEN_METEO_URL, OpenMeteoClient


@respx.mock
def test_fetch_current_parses_open_meteo_payload() -> None:
    city: City = {"City": "Berlin", "Latitude": 52.52, "Longitude": 13.405}
    route = respx.get(OPEN_METEO_URL).mock(
        return_value=httpx.Response(
            200,
            json={
                "current": {
                    "temperature_2m": 12.5,
                    "relative_humidity_2m": 70,
                    "wind_speed_10m": 3.2,
                }
            },
        )
    )

    client = OpenMeteoClient()
    rows = client.fetch_current([city])
    client.close()

    assert route.called
    assert rows == [
        {
            "City": "Berlin",
            "temperature_c": 12.5,
            "humidity": 70,
            "wind_speed_ms": 3.2,
        }
    ]

from jsonschema import validate
from forecast_api import get_forecast
from schemas import FORECAST_SCHEMA
import pytest 

def test_forecast_macthes_schema(api):
    response = get_forecast(api, 49.25, -123.12)
    assert response.status == 200
    validate(instance=response.json(), schema=FORECAST_SCHEMA)


CITIES = [
    (49.2497, -123.1193, "Vancouver"),
    (41.8781, -87.6298, "Chicago"),
    (35.6762, 139.6503, "Tokyo"),
    (-33.8688, 151.2093, "Sydney")
]

@pytest.mark.parametrize("latitude, longitude, city", CITIES)
def test_cities_schema(api, latitude, longitude, city):
    response = get_forecast(api, latitude, longitude)
    assert response.status == 200, f"{city}: {response.status} {response.text()}"
    validate(instance=response.json(), schema=FORECAST_SCHEMA)



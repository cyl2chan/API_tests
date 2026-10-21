from playwright.sync_api import APIRequestContext
from forecast_api import get_forecast

def test_first_forecast(api: APIRequestContext):
    response = get_forecast(
        # api = playwright.request.new_context()
        # response = api.get(
        #     "https://api.open-meteo.com/v1/forecast",
        #     params={"latitude": 49.25, "longitude": -122.85, "hourly": "temperature_2m"},
        # )
        api, 
        latitude = 49.25, 
        longitude = -122.85
    )

    print(response.status)
    print(response.headers["content-type"])
    print(response.json().keys())

    assert response.status == 200
    api.dispose()



import pytest
from forecast_api import get_forecast

CITIES = [
    (49.2497, -123.1193, "Vancouver"),
    (41.8781, -87.6298, "Chicago"),
    (35.6762, 139.6503, "Tokyo"),
    (-33.8688, 151.2093, "Sydney")
]

@pytest.mark.parametrize("latitude, longitude, city", CITIES)
def test_forecast_success(api, latitude, longitude, city):
    response = get_forecast(api, latitude, longitude)
    
    # 1. Status. The message prints the body, so a failure explains itself.
    print(response.text())
    assert response.status == 200, f"{city}: {response.status} {response.text()}"
    
    # 2. Header
    assert "application/json" in response.headers["content-type"]
    data = response.json()

    # 3. TODO: hourly.time and hourly.temperature_2m have the same length, and it isn't 0
    assert len(data["hourly"]["time"]) == len(data["hourly"]["temperature_2m"])

    # 4. TODO: the temperature unit is degrees Celsius "°C"(look at hourly_units)
    assert data["hourly_units"]["temperature_2m"] == "°C"

    # 5. TODO: the response is for the place you asked about (see below)
    assert round(data["latitude"], 0) == round(latitude, 0)


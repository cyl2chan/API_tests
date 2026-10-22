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
    #(49.2497, -123.1193, "Vancouver"),
    (49.2497, -123.1193, "Vancouver"),
    (41.8781, -87.6298, "Chicago"),
    (35.6762, 139.6503, "Tokyo"),
    (-33.8688, 151.2093, "Sydney")
]

@pytest.mark.parametrize("latitude, longitude, city", CITIES)
def test_forecast_success(api, latitude, longitude, city):
    response = get_forecast(api, latitude, longitude)
    
#   # 1. Status. The message prints the body, so a failure explains itself.
    assert response.status == 200, f"{city}: {response.status} {response.text()}"
    
#   # 2. Header
    assert "application/json" in response.headers["content-type"]
    data = response.json()

#   # 3. TODO: hourly.time and hourly.temperature_2m have the same length, and it isn't 0
    assert len(data["hourly"]["time"]) == len(data["hourly"]["temperature_2m"])

#   # 4. TODO: the temperature unit is degrees Celsius "°C"(look at hourly_units)
    assert data["hourly_units"]["temperature_2m"] == "°C"

#   # 5. TODO: the response is for the place you asked about (see below)
    assert round(data["latitude"], 0) == round(latitude, 0)


@pytest.mark.parametrize("invalid_lat", [91, -91, 999])
def test_invalid_latitude_rejected(api, invalid_lat):
    response = get_forecast(api, invalid_lat, 0)

    assert response.status == 400
    body = response.json()
    assert body["error"] is True
    print(body["reason"])
    assert body["reason"] # a non-empty explanation

# 1. A test that sends a misspelled variable, hourly="tempeture_2m", and checks it is rejected. 
# The docs show what the error looks like.
@pytest.mark.parametrize("misspelled", ["tempeture_2m"])
def test_misspelled(api, misspelled):
    response = get_forecast(api, 0, 0, hourly=misspelled)
    assert response.status == 400
    body = response.json()
    assert body["error"] is True
    assert body["reason"]

# 2. Add latitude 90 and -90 to your happy path test. 
# Predict first: should they pass? Run and record what happened.
@pytest.mark.parametrize("valid_lat", [90, -90])
def test_valid_lat(api, valid_lat):
    response = get_forecast(api, valid_lat, 0)
    assert response.status == 200

# 3. Find the valid range for longitude by experimenting in the browser, then write boundary tests for it: 
# the last valid value and the first invalid value on each side.
@pytest.mark.parametrize("test_long_val", [-180, 180]) #valid: 180, -180 invalid: 181, -181
def test_longitude_range(api, test_long_val):
    response = get_forecast(api, 0, test_long_val)
    assert response.status == 200
#valid range of longitude is -180 to 180




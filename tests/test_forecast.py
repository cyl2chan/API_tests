from playwright.sync_api import APIRequestContext
from forecast_api import get_forecast
import pytest
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


CITIES = [
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


def test_fahrenheit_unit(api):
    response = get_forecast(api, 49.25, -123.12, temperature_unit="fahrenheit")
    assert response.status == 200
    assert response.json()["hourly_units"]["temperature_2m"] == "°F"


Ask for three hourly variables in one request: temperature_2m,relative_humidity_2m,wind_speed_10m. 
Check each one appears in both hourly and hourly_units, and that all the arrays have the same length.
def test_hourly_var(api):
    response = get_forecast(api, 0, 0, hourly="temperature_2m,relative_humidity_2m,wind_speed_10m",
                            hourly_units="temperature_2m,relative_humidity_2m,wind_speed_10m", 
                            timezone="America/Vancouver")

    assert response.status == 200

    h_temp = response.json()["hourly"]["temperature_2m"]
    h_humidity =  response.json()["hourly"]["relative_humidity_2m"]
    h_wind =  response.json()["hourly"]["wind_speed_10m"]
    units_temp = response.json()["hourly_units"]["temperature_2m"]
    units_humidity =  response.json()["hourly_units"]["relative_humidity_2m"]
    units_wind =  response.json()["hourly_units"]["wind_speed_10m"]

    units_temp = "°F"   # need to also use formula to convert values of temp from C to F: (0°C × 9/5) + 32 = 32°F
    units_wind = "m/s"

    def convert_temp_to_F(h_temp):
        h_temp_F = []
        for temp_C in h_temp:
            temp_F = temp_C*9/5+32
            h_temp_F.append(round(temp_F, 1))
        return h_temp_F

    h_temp_F = convert_temp_to_F(h_temp)

    print(units_temp)
    print("temperature", h_temp_F, units_temp)

    timezone = response.json()["timezone"]
    utc_offset_seconds = response.json()["utc_offset_seconds"]

    # Check each one appears in both hourly and hourly_units
    assert h_temp
    assert h_humidity
    assert h_wind
    assert units_temp
    assert units_humidity
    assert units_wind
    assert units_wind == "m/s"
    assert timezone == "America/Vancouver"
    assert utc_offset_seconds == -25200

    # Check all the arrays have the same length
    assert len(h_temp) == len(h_humidity) == len(h_wind)


from jsonschema import validate
from schemas import FORECAST_SCHEMA
# write the tests. Hint: for a valid value, 
# check how many hourly entries come back. 
# Work out the expected count from forecast_days, and confirm your formula with one real request first.
# "-1,0,3,7,15,16,17,20,abc,;"
def test_forecast_days(api):
    response = get_forecast(api, 0, 0, forecast_days=1, hourly="temperature_2m")
    assert response.status == 200
    forecast_days = 1
    forecast_days_hours = forecast_days*24
    h_time = response.json()["hourly"]["time"]
    h_temp = response.json()["hourly"]["temperature_2m"]
    print("forecast hours:", forecast_days_hours, "; length of h_time:", len(h_time), "; length of h_temp:", len(h_temp))
    #print("; length of h_time:", len(h_time), "; length of h_temp:", len(h_temp))

    #assert h_time
    #assert h_temp
    assert len(h_time) == len(h_temp)
    assert len(h_time) == len(h_temp) == forecast_days_hours
    validate(instance=response.json(), schema=FORECAST_SCHEMA)
    #2, 3, 7, 15, 16: good
    #0: F. ass err, no h_time
    #-1, 17, 18, 20, abc, ;: F. 400
    # valid range of forecast days: 1-16 days
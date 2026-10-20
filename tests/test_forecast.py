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



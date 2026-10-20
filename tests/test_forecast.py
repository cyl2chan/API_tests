# tests/test_forecast.py
from playwright.sync_api import Playwright

def test_first_forecast(playwright: Playwright):
    api = playwright.request.new_context()
    response = api.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": 49.25, "longitude": -122.85, "hourly": "temperature_2m"},  
    )

    print(response.status)
    print(response.headers["content-type"])
    print(response.json().keys())

    assert response.status == 200
    api.dispose()



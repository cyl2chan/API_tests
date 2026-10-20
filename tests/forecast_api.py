from playwright.sync_api import APIRequestContext, APIResponse

FORECAST = "/v1/forecast"

def get_forecast(api: APIRequestContext, latitude, longitude, hourly="temperature_2m", **extra) -> APIResponse:
    params = {"latitude": latitude, "longitude": longitude, "hourly": hourly, **extra}
    return api.get(FORECAST, params=params)


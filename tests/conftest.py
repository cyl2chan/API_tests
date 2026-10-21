import os
import pytest
from playwright.sync_api import APIRequestContext, Playwright

BASE_URL = os.getenv("OPEN_METEO_BASE_URL", "https://api.open-meteo.com")

@pytest.fixture()#scope="session")
def api(playwright: Playwright) -> APIRequestContext:
    context = playwright.request.new_context(base_url=BASE_URL, timeout=10_000)
    yield context
    context.dispose()



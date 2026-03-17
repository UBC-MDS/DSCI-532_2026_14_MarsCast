import subprocess
import time
import os
import signal
import pytest
from playwright.sync_api import sync_playwright

APP_URL = "http://127.0.0.1:8001"

@pytest.fixture(scope="session", autouse=True)
def run_app():
    """Starts the Shiny app once for all UI tests so Playwright can interact with it reliably."""
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    proc = subprocess.Popen(
        ["shiny", "run", "src/app.py", "--port", "8001"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    time.sleep(2.5) #delay added
    yield
    proc.send_signal(signal.SIGINT)
    proc.wait(timeout=10)

def test_reset_button_restores_defaults():
    """Verifies Reset restores the default filter state so users can recover from complex filtering quickly."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(APP_URL)

        page.select_option("select#month", "Month 2")
        page.wait_for_timeout(500)

        # make sure the change happened first
        assert page.locator("select#month").input_value() == "Month 2"

        page.click("button#reset_all")

        # wait until reset is reflected in the DOM
        page.wait_for_function(
            "() => document.querySelector('select#month').value === 'All'"
        )

        assert page.locator("select#month").input_value() == "All"
        browser.close()

def test_season_filter_changes_kpi_value():
    """Verifies season filtering changes KPI outputs, proving seasonal slicing is connected to dashboard calculations."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(APP_URL)

        before = page.inner_text("#avg_min")
        initial_season = page.locator("select#season").input_value()
        new_season = "Winter" if initial_season != "Winter" else "Summer"

        page.select_option("select#season", new_season)
        page.wait_for_timeout(500)

        after = page.inner_text("#avg_min")
        assert before != after
        browser.close()

def test_month_filter_changes_kpi_value():
    """Verifies month filtering changes KPI outputs, proving filters are wired to computations."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(APP_URL)

        before = page.inner_text("#avg_pressure")

        initial_month = page.locator("select#month").input_value()
        new_month = "Month 1" if initial_month != "Month 1" else "Month 2"

        page.select_option("select#month", new_month)
        page.wait_for_timeout(500)

        after = page.inner_text("#avg_pressure")
        assert before != after
        browser.close()
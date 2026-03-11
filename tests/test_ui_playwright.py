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
        page = p.chromium.launch().new_page()
        page.goto(APP_URL)

        # change a filter (month)
        page.select_option("select#month", "Month 2")
        page.click("button#reset_all")

        # assert it returned to All
        assert page.query_selector("select#month").input_value() == "All"
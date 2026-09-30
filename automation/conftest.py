import pytest
import os
from playwright.sync_api import Page
from automation.config.config import BASE_URL, SCREENSHOTS_DIR, TRACES_DIR
from automation.fixtures.test_fixtures import auth_states, admin_page, hr_page, employee_page
from automation.utils.screenshots import capture_screenshot_on_failure

def pytest_configure(config):
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(TRACES_DIR, exist_ok=True)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot and trace on test failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page: Page = item.funcargs.get("page") or item.funcargs.get("admin_page") or item.funcargs.get("hr_page") or item.funcargs.get("employee_page")
        if page:
            screenshot_path = capture_screenshot_on_failure(page, item.name, SCREENSHOTS_DIR)
            print(f"\n[FAILURE SCREENSHOT SAVED]: {screenshot_path}")
            
            # Attach screenshot to html report if pytest-html installed
            if hasattr(report, "extra"):
                pytest_html = item.config.pluginmanager.getplugin("html")
                if pytest_html:
                    extra = getattr(report, "extra", [])
                    extra.append(pytest_html.extras.image(screenshot_path))
                    report.extra = extra

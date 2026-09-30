import os
from datetime import datetime
from playwright.sync_api import Page

def capture_screenshot_on_failure(page: Page, test_name: str, screenshots_dir: str) -> str:
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_test_name = test_name.replace("/", "_").replace("::", "_").replace(".py", "")
    filename = f"FAILED_{clean_test_name}_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)
    page.screenshot(path=filepath, full_page=True)
    return filepath

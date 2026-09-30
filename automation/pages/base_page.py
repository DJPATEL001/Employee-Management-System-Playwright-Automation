from playwright.sync_api import Page, Locator
from automation.config.config import BASE_URL

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.nav_dashboard: Locator = page.get_by_test_id("nav-dashboard")
        self.nav_employees: Locator = page.get_by_test_id("nav-employees")
        self.nav_add_employee: Locator = page.get_by_test_id("nav-add-employee")
        self.nav_documents: Locator = page.get_by_test_id("nav-documents")
        self.nav_profile: Locator = page.get_by_test_id("nav-profile")
        self.logout_button: Locator = page.get_by_test_id("nav-logout")

        self.success_message: Locator = page.get_by_test_id("success-message")
        self.error_message: Locator = page.get_by_test_id("error-message")

    def navigate_to(self, endpoint: str = ""):
        url = f"{BASE_URL}{endpoint}" if endpoint.startswith("/") else f"{BASE_URL}/{endpoint}"
        self.page.goto(url)

    def logout(self):
        if self.logout_button.is_visible():
            self.logout_button.click()

    def get_success_message_text(self) -> str:
        return self.success_message.inner_text() if self.success_message.is_visible() else ""

    def get_error_message_text(self) -> str:
        return self.error_message.inner_text() if self.error_message.is_visible() else ""

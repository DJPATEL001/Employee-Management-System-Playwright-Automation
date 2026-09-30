from playwright.sync_api import Page, Locator
from automation.pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input: Locator = page.get_by_test_id("login-email")
        self.password_input: Locator = page.get_by_test_id("login-password")
        self.login_button: Locator = page.get_by_test_id("login-button")

    def navigate(self):
        self.navigate_to("/login")

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

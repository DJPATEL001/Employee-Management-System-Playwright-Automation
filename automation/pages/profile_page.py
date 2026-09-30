from playwright.sync_api import Page, Locator
from automation.pages.base_page import BasePage

class ProfilePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.profile_name_header: Locator = page.get_by_test_id("profile-name-header")
        self.profile_role: Locator = page.get_by_test_id("profile-role")
        self.profile_email: Locator = page.get_by_test_id("profile-email")

        self.phone_input: Locator = page.get_by_test_id("profile-phone-input")
        self.address_input: Locator = page.get_by_test_id("profile-address-input")
        self.update_button: Locator = page.get_by_test_id("update-profile-button")

    def navigate(self):
        self.navigate_to("/profile")

    def update_profile(self, phone: str, address: str):
        self.phone_input.fill(phone)
        self.address_input.fill(address)
        self.update_button.click()

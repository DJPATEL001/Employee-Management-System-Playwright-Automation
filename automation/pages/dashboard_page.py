from playwright.sync_api import Page, Locator
from automation.pages.base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.stat_total_employees: Locator = page.get_by_test_id("stat-total-employees")
        self.stat_active_employees: Locator = page.get_by_test_id("stat-active-employees")
        self.stat_inactive_employees: Locator = page.get_by_test_id("stat-inactive-employees")
        self.stat_departments: Locator = page.get_by_test_id("stat-departments")
        self.add_employee_btn: Locator = page.get_by_test_id("add-employee-button")

    def navigate(self):
        self.navigate_to("/dashboard")

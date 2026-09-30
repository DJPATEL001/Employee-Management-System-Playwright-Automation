from playwright.sync_api import Page, Locator
from automation.pages.base_page import BasePage

class EmployeeListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input: Locator = page.get_by_test_id("employee-search")
        self.department_filter: Locator = page.get_by_test_id("department-filter")
        self.status_filter: Locator = page.get_by_test_id("status-filter")
        self.position_filter: Locator = page.get_by_test_id("position-filter")
        self.add_employee_btn: Locator = page.get_by_test_id("add-employee-button")
        
        self.employee_table: Locator = page.get_by_test_id("employee-table")
        self.employee_rows: Locator = page.get_by_test_id("employee-row")

        self.delete_modal: Locator = page.get_by_test_id("delete-modal")
        self.confirm_delete_btn: Locator = page.get_by_test_id("confirm-delete")
        self.cancel_delete_btn: Locator = page.get_by_test_id("cancel-delete")

    def navigate(self):
        self.navigate_to("/employees")

    def search_employee(self, term: str):
        self.search_input.fill(term)

    def filter_by_department(self, dept: str):
        self.department_filter.select_option(dept)

    def filter_by_status(self, status: str):
        self.status_filter.select_option(status)

    def click_delete_employee(self, employee_id: int):
        btn = self.page.locator(f"[data-testid-id='delete-employee-{employee_id}']")
        btn.click()

    def confirm_delete(self):
        self.confirm_delete_btn.click()

    def cancel_delete(self):
        self.cancel_delete_btn.click()

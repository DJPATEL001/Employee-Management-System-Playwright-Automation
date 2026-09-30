from playwright.sync_api import Page, Locator
from automation.pages.base_page import BasePage

class EmployeeFormPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input: Locator = page.get_by_test_id("first-name-input")
        self.last_name_input: Locator = page.get_by_test_id("last-name-input")
        self.email_input: Locator = page.get_by_test_id("email-input")
        self.phone_input: Locator = page.get_by_test_id("phone-input")
        self.department_select: Locator = page.get_by_test_id("department-select")
        self.position_input: Locator = page.get_by_test_id("position-input")
        self.joining_date_input: Locator = page.get_by_test_id("joining-date-input")
        self.salary_input: Locator = page.get_by_test_id("salary-input")
        self.status_select: Locator = page.get_by_test_id("status-select")
        self.address_input: Locator = page.get_by_test_id("address-input")
        self.submit_button: Locator = page.get_by_test_id("submit-employee-button")

    def navigate_add(self):
        self.navigate_to("/employees/add")

    def navigate_edit(self, employee_id: int):
        self.navigate_to(f"/employees/{employee_id}/edit")

    def fill_employee_form(self, data: dict):
        if "first_name" in data:
            self.first_name_input.fill(data["first_name"])
        if "last_name" in data:
            self.last_name_input.fill(data["last_name"])
        if "email" in data:
            self.email_input.fill(data["email"])
        if "phone" in data:
            self.phone_input.fill(data["phone"])
        if "department" in data and data["department"]:
            self.department_select.select_option(data["department"])
        if "position" in data:
            self.position_input.fill(data["position"])
        if "joining_date" in data:
            self.joining_date_input.fill(data["joining_date"])
        if "salary" in data:
            self.salary_input.fill(data["salary"])
        if "status" in data:
            self.status_select.select_option(data["status"])
        if "address" in data:
            self.address_input.fill(data["address"])

    def submit_form(self):
        self.submit_button.click()

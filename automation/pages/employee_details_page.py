from playwright.sync_api import Page, Locator
from automation.pages.base_page import BasePage

class EmployeeDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.detail_name: Locator = page.get_by_test_id("detail-name")
        self.detail_email: Locator = page.get_by_test_id("detail-email")
        self.detail_phone: Locator = page.get_by_test_id("detail-phone")
        self.detail_department: Locator = page.get_by_test_id("detail-department")
        self.detail_position: Locator = page.get_by_test_id("detail-position")
        self.detail_status: Locator = page.get_by_test_id("detail-status")

        self.file_input: Locator = page.get_by_test_id("file-upload")
        self.upload_button: Locator = page.get_by_test_id("upload-button")
        self.document_list: Locator = page.get_by_test_id("document-list")
        self.document_items: Locator = page.get_by_test_id("document-item")

    def navigate(self, employee_id: int):
        self.navigate_to(f"/employees/{employee_id}")

    def upload_document(self, file_path: str):
        self.file_input.set_input_files(file_path)
        self.upload_button.click()

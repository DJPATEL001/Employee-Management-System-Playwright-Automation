import pytest
import re
from playwright.sync_api import Page, expect
from automation.pages.employee_list_page import EmployeeListPage
from automation.pages.employee_form_page import EmployeeFormPage
from automation.pages.employee_details_page import EmployeeDetailsPage
from automation.utils.helpers import generate_random_email, generate_random_phone

def test_employee_list_loads(admin_page: Page):
    """TC_EMP_015: Employee Directory table loads with headers and records."""
    emp_list = EmployeeListPage(admin_page)
    emp_list.navigate()
    expect(emp_list.employee_table).to_be_visible()
    expect(emp_list.employee_rows.first).to_be_visible()

def test_search_employee_by_name(admin_page: Page):
    """TC_EMP_016: Searching by name filters table to matching employee."""
    emp_list = EmployeeListPage(admin_page)
    emp_list.navigate()
    emp_list.search_employee("Alexander")
    
    visible_row = admin_page.locator("[data-testid='employee-row']:visible")
    expect(visible_row).to_contain_text("Alexander Wright")

def test_search_employee_by_email(admin_page: Page):
    """TC_EMP_017: Searching by email filters table to matching employee."""
    emp_list = EmployeeListPage(admin_page)
    emp_list.navigate()
    emp_list.search_employee("sarah.jenkins@workforce.test")
    
    visible_row = admin_page.locator("[data-testid='employee-row']:visible")
    expect(visible_row).to_contain_text("Sarah Jenkins")

def test_search_invalid_employee(admin_page: Page):
    """TC_EMP_019: Searching for non-existent name hides all rows."""
    emp_list = EmployeeListPage(admin_page)
    emp_list.navigate()
    emp_list.search_employee("NonExistentTerm999")
    
    visible_rows = admin_page.locator("[data-testid='employee-row']:visible")
    expect(visible_rows).to_have_count(0)

def test_department_filter(admin_page: Page):
    """TC_EMP_020: Filtering by department isolates department personnel."""
    emp_list = EmployeeListPage(admin_page)
    emp_list.navigate()
    emp_list.filter_by_department("Engineering")
    
    visible_rows = admin_page.locator("[data-testid='employee-row']:visible")
    expect(visible_rows.first).to_contain_text("Engineering")

def test_status_filter(admin_page: Page):
    """TC_EMP_021 & 022: Filtering by Active/Inactive status isolates rows."""
    emp_list = EmployeeListPage(admin_page)
    emp_list.navigate()
    emp_list.filter_by_status("Inactive")
    
    visible_rows = admin_page.locator("[data-testid='employee-row']:visible")
    expect(visible_rows.first).to_contain_text("Inactive")

def test_view_employee_details(admin_page: Page):
    """Navigate to Employee details view."""
    emp_list = EmployeeListPage(admin_page)
    emp_list.navigate()
    admin_page.locator("[data-testid-id='view-employee-1']").click()
    
    details_page = EmployeeDetailsPage(admin_page)
    expect(admin_page).to_have_url("http://127.0.0.1:8000/employees/1")
    expect(details_page.detail_name).to_contain_text("Alexander Wright")

def test_add_new_employee_success(admin_page: Page):
    """TC_CRUD_025: Create new employee with valid parameters."""
    form_page = EmployeeFormPage(admin_page)
    form_page.navigate_add()

    email = generate_random_email()
    phone = generate_random_phone()

    data = {
        "first_name": "TestFirst",
        "last_name": "TestLast",
        "email": email,
        "phone": phone,
        "department": "Engineering",
        "position": "Automation Engineer",
        "joining_date": "2024-02-01",
        "salary": "95000",
        "status": "Active",
        "address": "123 Automation Lane"
    }

    form_page.fill_employee_form(data)
    form_page.submit_form()

    expect(form_page.success_message).to_be_visible()
    expect(form_page.success_message).to_contain_text("Employee created successfully")

def test_edit_employee_success(admin_page: Page):
    """TC_CRUD_032: Edit employee position and address."""
    form_page = EmployeeFormPage(admin_page)
    form_page.navigate_edit(1)

    form_page.fill_employee_form({"position": "Chief Enterprise Architect"})
    form_page.submit_form()

    expect(admin_page).to_have_url("http://127.0.0.1:8000/employees/1?success=Employee+updated+successfully")

def test_delete_employee_modal_cancel_and_confirm(admin_page: Page):
    """TC_CRUD_034 & 035: Test delete confirmation modal cancel and confirm paths."""
    # First create temporary employee to delete
    form_page = EmployeeFormPage(admin_page)
    form_page.navigate_add()
    email = generate_random_email()
    phone = generate_random_phone()
    form_page.fill_employee_form({
        "first_name": "TempToDelete",
        "last_name": "User",
        "email": email,
        "phone": phone,
        "department": "Finance",
        "position": "Temp Analyst",
        "joining_date": "2024-03-01",
        "salary": "50000",
        "status": "Active",
        "address": "123 Temp St"
    })
    form_page.submit_form()

    emp_list = EmployeeListPage(admin_page)
    emp_list.navigate()
    emp_list.search_employee("TempToDelete")

    delete_btn = admin_page.locator("[data-testid='delete-employee']:visible").first
    delete_btn.click()

    # Cancel path
    expect(admin_page.locator("#delete-modal.active")).to_be_visible()
    emp_list.cancel_delete()
    expect(admin_page.locator("#delete-modal.active")).not_to_be_visible()

    # Confirm path
    delete_btn.click()
    expect(admin_page.locator("#delete-modal.active")).to_be_visible()
    emp_list.confirm_delete()

    expect(admin_page).to_have_url("http://127.0.0.1:8000/employees?success=Employee+deleted+successfully")

import pytest
from playwright.sync_api import Page, expect
from automation.pages.employee_list_page import EmployeeListPage

def test_admin_full_permissions(admin_page: Page):
    """TC_RBAC_036: Admin role has full visibility including Delete buttons."""
    emp_list = EmployeeListPage(admin_page)
    emp_list.navigate()

    expect(emp_list.nav_add_employee).to_be_visible()
    expect(admin_page.locator("[data-testid='delete-employee']").first).to_be_visible()

def test_hr_manager_delete_button_absence(hr_page: Page):
    """TC_RBAC_037: HR Manager can Add/Edit but Delete buttons are hidden."""
    emp_list = EmployeeListPage(hr_page)
    emp_list.navigate()

    expect(emp_list.nav_add_employee).to_be_visible()
    expect(hr_page.locator("[data-testid='delete-employee']")).to_have_count(0)

def test_hr_manager_direct_delete_forbidden(hr_page: Page):
    """TC_RBAC_038: HR Manager attempting direct delete is blocked."""
    # Attempt to post to delete endpoint directly using page evaluate / fetch
    response = hr_page.request.post("http://127.0.0.1:8000/employees/1/delete")
    # Response redirects to /employees?error=Only+Admin+can+delete+employees
    assert "Only+Admin+can+delete+employees" in response.url or response.status == 302

def test_employee_access_restrictions(employee_page: Page):
    """TC_RBAC_039 & 040: Employee user cannot access Employee Directory or Dashboard."""
    employee_page.goto("http://127.0.0.1:8000/employees")
    expect(employee_page).to_have_url("http://127.0.0.1:8000/profile")

    employee_page.goto("http://127.0.0.1:8000/dashboard")
    expect(employee_page).to_have_url("http://127.0.0.1:8000/profile")

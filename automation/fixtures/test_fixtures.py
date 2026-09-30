import pytest
import os
from playwright.sync_api import Browser, BrowserContext, Page
from automation.config.config import (
    BASE_URL, ADMIN_EMAIL, ADMIN_PASSWORD, HR_EMAIL, HR_PASSWORD, EMPLOYEE_EMAIL, EMPLOYEE_PASSWORD,
    AUTH_DIR
)
from automation.pages.login_page import LoginPage
from automation.pages.dashboard_page import DashboardPage
from automation.pages.employee_list_page import EmployeeListPage
from automation.pages.employee_form_page import EmployeeFormPage
from automation.pages.employee_details_page import EmployeeDetailsPage
from automation.pages.profile_page import ProfilePage

@pytest.fixture(scope="session")
def auth_states(browser: Browser):
    """Generate and store storage state for Admin, HR Manager, and Employee roles."""
    os.makedirs(AUTH_DIR, exist_ok=True)

    admin_state_path = os.path.join(AUTH_DIR, "admin_state.json")
    hr_state_path = os.path.join(AUTH_DIR, "hr_state.json")
    employee_state_path = os.path.join(AUTH_DIR, "employee_state.json")

    # 1. Admin Login & Save State
    context = browser.new_context(base_url=BASE_URL)
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    page.wait_for_url("**/dashboard")
    context.storage_state(path=admin_state_path)
    context.close()

    # 2. HR Manager Login & Save State
    context = browser.new_context(base_url=BASE_URL)
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(HR_EMAIL, HR_PASSWORD)
    page.wait_for_url("**/dashboard")
    context.storage_state(path=hr_state_path)
    context.close()

    # 3. Employee Login & Save State
    context = browser.new_context(base_url=BASE_URL)
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(EMPLOYEE_EMAIL, EMPLOYEE_PASSWORD)
    page.wait_for_url("**/profile")
    context.storage_state(path=employee_state_path)
    context.close()

    return {
        "admin": admin_state_path,
        "hr": hr_state_path,
        "employee": employee_state_path
    }

@pytest.fixture
def admin_page(browser: Browser, auth_states):
    """Fixture providing a Page authenticated as Admin."""
    context = browser.new_context(
        base_url=BASE_URL,
        storage_state=auth_states["admin"]
    )
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def hr_page(browser: Browser, auth_states):
    """Fixture providing a Page authenticated as HR Manager."""
    context = browser.new_context(
        base_url=BASE_URL,
        storage_state=auth_states["hr"]
    )
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture
def employee_page(browser: Browser, auth_states):
    """Fixture providing a Page authenticated as Employee."""
    context = browser.new_context(
        base_url=BASE_URL,
        storage_state=auth_states["employee"]
    )
    page = context.new_page()
    yield page
    context.close()

import pytest
import re
from playwright.sync_api import Page, expect
from automation.config.config import ADMIN_EMAIL, ADMIN_PASSWORD, HR_EMAIL, HR_PASSWORD, EMPLOYEE_EMAIL, EMPLOYEE_PASSWORD
from automation.pages.login_page import LoginPage

def test_valid_admin_login(page: Page):
    """TC_LOG_001: Valid Admin login redirects to /dashboard with Admin badge."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    expect(page).to_have_url(re.compile(r".*/dashboard"))
    expect(page.get_by_text("Admin", exact=True)).to_be_visible()

def test_valid_hr_login(page: Page):
    """TC_LOG_002: Valid HR Manager login redirects to /dashboard with HR Manager badge."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(HR_EMAIL, HR_PASSWORD)
    expect(page).to_have_url(re.compile(r".*/dashboard"))
    expect(page.get_by_text("HR Manager", exact=True)).to_be_visible()

def test_valid_employee_login(page: Page):
    """TC_LOG_003: Valid Employee login redirects to /profile."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(EMPLOYEE_EMAIL, EMPLOYEE_PASSWORD)
    expect(page).to_have_url(re.compile(r".*/profile"))
    expect(page.get_by_test_id("profile-role")).to_have_text("Employee")

def test_invalid_password(page: Page):
    """TC_LOG_004: Invalid password shows validation error message."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(ADMIN_EMAIL, "WrongPassword123")
    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text("Invalid email or password")

def test_invalid_email(page: Page):
    """TC_LOG_005: Non-existent email shows error message."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("nonexistent@workforce.test", "Admin@12345")
    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text("Invalid email or password")

def test_empty_email(page: Page):
    """TC_LOG_006: Empty email field shows validation error."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("", ADMIN_PASSWORD)
    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text("Email is required")

def test_empty_password(page: Page):
    """TC_LOG_007: Empty password field shows validation error."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(ADMIN_EMAIL, "")
    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text("Password is required")

def test_invalid_email_format(page: Page):
    """TC_LOG_008: Malformed email format shows validation error."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("invalidemailformat", ADMIN_PASSWORD)
    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text("Invalid email format")

def test_user_logout(page: Page):
    """TC_LOG_009: Logging out clears session and redirects to /login."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    expect(page).to_have_url(re.compile(r".*/dashboard"))
    
    login_page.logout()
    expect(page).to_have_url(re.compile(r".*/login\?msg=Logged\+out\+successfully"))

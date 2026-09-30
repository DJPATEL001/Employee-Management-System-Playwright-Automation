import pytest
from playwright.sync_api import Page, expect
from automation.pages.employee_form_page import EmployeeFormPage
from automation.utils.helpers import generate_random_email, generate_random_phone

def test_validation_required_fields(admin_page: Page):
    """TC_VAL_026: Submitting form with missing required fields triggers error."""
    form_page = EmployeeFormPage(admin_page)
    form_page.navigate_add()

    # Fill form except First Name
    form_page.fill_employee_form({
        "first_name": "",
        "last_name": "Smith",
        "email": generate_random_email(),
        "phone": generate_random_phone(),
        "department": "HR",
        "position": "Specialist",
        "joining_date": "2024-01-01",
        "salary": "60000",
        "status": "Active",
        "address": "Address"
    })
    form_page.submit_form()

    expect(form_page.error_message).to_be_visible()
    expect(form_page.error_message).to_contain_text("First Name is required")

def test_validation_invalid_email(admin_page: Page):
    """TC_VAL_027: Malformed email format triggers error."""
    form_page = EmployeeFormPage(admin_page)
    form_page.navigate_add()

    form_page.fill_employee_form({
        "first_name": "Bad",
        "last_name": "Email",
        "email": "notanemailaddress",
        "phone": generate_random_phone(),
        "department": "Finance",
        "position": "Analyst",
        "joining_date": "2024-01-01",
        "salary": "70000",
        "status": "Active",
        "address": "Address"
    })
    form_page.submit_form()

    expect(form_page.error_message).to_be_visible()
    expect(form_page.error_message).to_contain_text("Invalid email format")

def test_validation_invalid_phone(admin_page: Page):
    """TC_VAL_028: Invalid phone format triggers error."""
    form_page = EmployeeFormPage(admin_page)
    form_page.navigate_add()

    form_page.fill_employee_form({
        "first_name": "Short",
        "last_name": "Phone",
        "email": generate_random_email(),
        "phone": "12345",
        "department": "Sales",
        "position": "Rep",
        "joining_date": "2024-01-01",
        "salary": "50000",
        "status": "Active",
        "address": "Address"
    })
    form_page.submit_form()

    expect(form_page.error_message).to_be_visible()
    expect(form_page.error_message).to_contain_text("Invalid phone number format")

def test_validation_invalid_salary(admin_page: Page):
    """TC_VAL_029: Non-numeric salary input triggers error."""
    form_page = EmployeeFormPage(admin_page)
    form_page.navigate_add()

    form_page.fill_employee_form({
        "first_name": "Non",
        "last_name": "Numeric",
        "email": generate_random_email(),
        "phone": generate_random_phone(),
        "department": "Marketing",
        "position": "Lead",
        "joining_date": "2024-01-01",
        "salary": "INVALID_SALARY_TEXT",
        "status": "Active",
        "address": "Address"
    })
    form_page.submit_form()

    expect(form_page.error_message).to_be_visible()
    expect(form_page.error_message).to_contain_text("Salary must be a valid positive number")

def test_validation_duplicate_email(admin_page: Page):
    """TC_VAL_031: Duplicate email address triggers conflict error."""
    form_page = EmployeeFormPage(admin_page)
    form_page.navigate_add()

    form_page.fill_employee_form({
        "first_name": "Duplicate",
        "last_name": "EmailUser",
        "email": "alexander.wright@workforce.test",
        "phone": generate_random_phone(),
        "department": "Engineering",
        "position": "Developer",
        "joining_date": "2024-01-01",
        "salary": "80000",
        "status": "Active",
        "address": "Address"
    })
    form_page.submit_form()

    expect(form_page.error_message).to_be_visible()
    expect(form_page.error_message).to_contain_text("Employee with this email already exists")

def test_validation_invalid_date(admin_page: Page):
    """TC_VAL_030: Invalid joining date format triggers error."""
    form_page = EmployeeFormPage(admin_page)
    form_page.navigate_add()

    form_page.fill_employee_form({
        "first_name": "Bad",
        "last_name": "Date",
        "email": generate_random_email(),
        "phone": generate_random_phone(),
        "department": "HR",
        "position": "Assistant",
        "joining_date": "2026-02-31",
        "salary": "50000",
        "status": "Active",
        "address": "Address"
    })
    form_page.submit_form()

    expect(form_page.error_message).to_be_visible()
    expect(form_page.error_message).to_contain_text("Invalid joining date format")

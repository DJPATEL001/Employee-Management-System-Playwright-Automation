import pytest
from playwright.sync_api import Page, expect
from automation.pages.profile_page import ProfilePage

def test_view_employee_profile(employee_page: Page):
    """View logged in user profile details."""
    profile = ProfilePage(employee_page)
    profile.navigate()

    expect(profile.profile_name_header).to_contain_text("John Doe")
    expect(profile.profile_role).to_contain_text("Employee")
    expect(profile.profile_email).to_contain_text("employee@workforce.test")

def test_update_employee_profile_contact(employee_page: Page):
    """Employee updates own phone and address contact details."""
    profile = ProfilePage(employee_page)
    profile.navigate()

    new_phone = "9876543299"
    new_address = "777 Updated Sunset Boulevard, Eugene, OR"

    profile.update_profile(new_phone, new_address)

    expect(profile.success_message).to_be_visible()
    expect(profile.success_message).to_contain_text("Profile updated successfully")
    expect(profile.phone_input).to_have_value(new_phone)

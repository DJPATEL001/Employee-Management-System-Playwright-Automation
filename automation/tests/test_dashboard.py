import pytest
from playwright.sync_api import Page, expect
from automation.pages.dashboard_page import DashboardPage

def test_dashboard_loads(admin_page: Page):
    """TC_DSH_010: Dashboard loads correctly for authenticated Admin."""
    dashboard = DashboardPage(admin_page)
    dashboard.navigate()
    expect(admin_page).to_have_title("Dashboard - WorkForce HR")
    expect(admin_page.get_by_role("heading", name="Admin Dashboard")).to_be_visible()

def test_statistics_cards_display(admin_page: Page):
    """TC_DSH_011 & 012: Verify statistics metric cards display valid values."""
    dashboard = DashboardPage(admin_page)
    dashboard.navigate()

    expect(dashboard.stat_total_employees).to_be_visible()
    expect(dashboard.stat_active_employees).to_be_visible()
    expect(dashboard.stat_inactive_employees).to_be_visible()
    expect(dashboard.stat_departments).to_be_visible()

    total_text = dashboard.stat_total_employees.inner_text()
    assert int(total_text) > 0, "Total employees should be greater than 0"

def test_dashboard_navigation_links(admin_page: Page):
    """TC_DSH_014: Dashboard navigation header links are functional."""
    dashboard = DashboardPage(admin_page)
    dashboard.navigate()

    expect(dashboard.nav_dashboard).to_be_visible()
    expect(dashboard.nav_employees).to_be_visible()
    expect(dashboard.nav_add_employee).to_be_visible()
    expect(dashboard.nav_documents).to_be_visible()
    expect(dashboard.nav_profile).to_be_visible()

def test_navigate_to_employees_from_dashboard(admin_page: Page):
    """Navigate to Employee directory via dashboard link."""
    dashboard = DashboardPage(admin_page)
    dashboard.navigate()
    admin_page.get_by_text("View All Employees →").click()
    expect(admin_page).to_have_url("http://127.0.0.1:8000/employees")

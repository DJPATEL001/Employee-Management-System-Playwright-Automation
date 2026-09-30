import pytest
import os
from playwright.sync_api import Page, expect
from automation.pages.employee_details_page import EmployeeDetailsPage

@pytest.fixture
def temp_upload_files(tmp_path):
    pdf_path = tmp_path / "test_resume.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 Test Resume Document Body")

    png_path = tmp_path / "test_id.png"
    png_path.write_bytes(b"\x89PNG\r\n\x1a\nFakePNGHeaderData")

    jpg_path = tmp_path / "test_photo.jpg"
    jpg_path.write_bytes(b"\xff\xd8\xffFakeJPGHeaderData")

    exe_path = tmp_path / "test_script.exe"
    exe_path.write_bytes(b"MZExecutableHeaderData")

    return {
        "pdf": str(pdf_path),
        "png": str(png_path),
        "jpg": str(jpg_path),
        "exe": str(exe_path)
    }

def test_upload_valid_pdf(admin_page: Page, temp_upload_files):
    """TC_DOC_041: Upload valid PDF document."""
    details = EmployeeDetailsPage(admin_page)
    details.navigate(1)
    details.upload_document(temp_upload_files["pdf"])

    expect(admin_page).to_have_url("http://127.0.0.1:8000/employees/1?success=Document+uploaded+successfully")
    expect(details.document_list).to_contain_text("test_resume.pdf")

def test_upload_valid_png(admin_page: Page, temp_upload_files):
    """TC_DOC_042: Upload valid PNG image."""
    details = EmployeeDetailsPage(admin_page)
    details.navigate(1)
    details.upload_document(temp_upload_files["png"])

    expect(admin_page).to_have_url("http://127.0.0.1:8000/employees/1?success=Document+uploaded+successfully")
    expect(details.document_list).to_contain_text("test_id.png")

def test_upload_valid_jpg(admin_page: Page, temp_upload_files):
    """TC_DOC_043: Upload valid JPG image."""
    details = EmployeeDetailsPage(admin_page)
    details.navigate(1)
    details.upload_document(temp_upload_files["jpg"])

    expect(admin_page).to_have_url("http://127.0.0.1:8000/employees/1?success=Document+uploaded+successfully")
    expect(details.document_list).to_contain_text("test_photo.jpg")

def test_upload_invalid_file_type(admin_page: Page, temp_upload_files):
    """TC_DOC_044: Uploading disallowed file format (.exe) shows error banner."""
    details = EmployeeDetailsPage(admin_page)
    details.navigate(1)
    details.upload_document(temp_upload_files["exe"])

    expect(admin_page).to_have_url("http://127.0.0.1:8000/employees/1?error=Invalid+file+format.+Allowed+formats:+PDF,+PNG,+JPG")
    expect(details.error_message).to_be_visible()
    expect(details.error_message).to_contain_text("Invalid file format")

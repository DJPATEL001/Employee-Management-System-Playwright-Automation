# Bug Reports — WorkForce HR Employee Management System

This document contains 5 realistic, reproducible bug reports logged during the manual testing phase of the WorkForce HR system.

---

## Bug Report #1: BUG-001

* **Bug ID**: `BUG-001`
* **Title**: Employee table search by phone number fails to return matching results
* **Module**: Employee Directory / Search
* **Preconditions**:
  1. User is logged in as Admin (`admin@workforce.test`).
  2. Employee list contains record with phone number `9876543212` (John Doe).
* **Steps to Reproduce**:
  1. Navigate to `/employees`.
  2. In the search input field (`data-testid="employee-search"`), enter `9876543212`.
  3. Observe table rows.
* **Expected Result**: The employee table should filter and display John Doe (`EMP003`).
* **Actual Result**: All employee rows are hidden because search filter client script only checks employee code, name, and email fields.
* **Severity**: Medium
* **Priority**: P2
* **Environment**: Windows 11, Chrome 124, Web App v1.0 (Local SQLite)
* **Status**: Open

---

## Bug Report #2: BUG-002

* **Bug ID**: `BUG-002`
* **Title**: Adding employee with phone number containing spaces fails validation incorrectly
* **Module**: Add Employee Form / Validation
* **Preconditions**:
  1. User is logged in as HR Manager (`hr@workforce.test`).
* **Steps to Reproduce**:
  1. Navigate to `/employees/add`.
  2. Fill out all valid fields, but enter phone number with international spacing e.g., `+1 987 654 3210`.
  3. Click "Create Employee" button.
* **Expected Result**: System should sanitize spacing or accept valid phone string with spaces and create employee.
* **Actual Result**: Form fails with error message `"Invalid phone number format"`.
* **Severity**: Low
* **Priority**: P3
* **Environment**: Windows 11, Edge 124, Web App v1.0
* **Status**: Open

---

## Bug Report #3: BUG-003

* **Bug ID**: `BUG-003`
* **Title**: Document upload accepts file with uppercase extension `.PDF` but displays incorrect mime tag in UI
* **Module**: Document Upload
* **Preconditions**:
  1. User is logged in as Admin (`admin@workforce.test`).
  2. User is on employee details page `/employees/3`.
* **Steps to Reproduce**:
  1. Select file named `Offer_Letter.PDF` (uppercase extension).
  2. Click "Upload File" button.
* **Expected Result**: File should upload successfully and display file type `PDF`.
* **Actual Result**: File is uploaded but file_type is stored as `JPG` fallback due to strict lower case string match condition in file extension handler.
* **Severity**: Medium
* **Priority**: P2
* **Environment**: Windows 11, Firefox 125, Web App v1.0
* **Status**: Open

---

## Bug Report #4: BUG-004

* **Bug ID**: `BUG-004`
* **Title**: Employee role user can access `/documents` hub page but sees empty list without error guidance
* **Module**: Role Access / Documents Hub
* **Preconditions**:
  1. User is logged in as Employee (`employee@workforce.test`).
  2. Employee has 0 uploaded documents.
* **Steps to Reproduce**:
  1. Click "Documents" link in top navbar (`data-testid="nav-documents"`).
  2. Observe page content.
* **Expected Result**: Displays message `"You currently have no uploaded documents. Please contact HR to upload records."`.
* **Actual Result**: Displays generic `"No documents found in repository"` without explaining role context.
* **Severity**: Low
* **Priority**: P3
* **Environment**: Windows 11, Chrome 124, Web App v1.0
* **Status**: Open

---

## Bug Report #5: BUG-005

* **Bug ID**: `BUG-005`
* **Title**: Dashboard recent employees table displays unformatted joining date string
* **Module**: Admin Dashboard
* **Preconditions**:
  1. User is logged in as Admin (`admin@workforce.test`).
* **Steps to Reproduce**:
  1. Navigate to `/dashboard`.
  2. Inspect Recent Employees table.
* **Expected Result**: Joining Date column should render formatted date e.g., `Mar 15, 2021` or `2021-03-15`.
* **Actual Result**: Raw date format or missing joining date column in recent employees table view.
* **Severity**: Low
* **Priority**: P3
* **Environment**: Windows 11, Chrome 124, Web App v1.0
* **Status**: Open

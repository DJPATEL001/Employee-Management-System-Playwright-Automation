# Test Plan — WorkForce HR Employee Management System

## 1. Objective
The primary objective of this Test Plan is to outline the scope, strategy, environment, entry/exit criteria, and test types for validating the **WorkForce HR Employee Management System**. The goal is to ensure high application quality, robust security, strict role-based access control (RBAC), data integrity, and a flawless user experience across all core modules.

---

## 2. Scope

### In-Scope
* **Authentication & Session Management**: Login, logout, credential validation, empty field checks, email format checks, role-based post-login redirection.
* **Dashboard Module**: Metrics cards accuracy (total, active, inactive, departments), recent employee records display, navigation links.
* **Employee Management Module**: Employee listing, searching (by ID, Name, Email), filtering (by Department, Status, Position), pagination/row limits.
* **Employee CRUD Operations**: Adding new employee, editing existing employee details, deleting employee (Admin only) with confirmation modal.
* **Data Validation Engine**: Required field checks, duplicate email prevention, phone format verification, salary numeric bounds, valid joining date formats.
* **Role-Based Access Control (RBAC)**:
  * **Admin**: Full access (View, Add, Edit, Delete, Upload Docs).
  * **HR Manager**: Partial management (View, Add, Edit, Upload Docs; No Delete).
  * **Employee**: Self-service profile (View own details/documents, limited contact updates).
* **Document Upload Module**: File type validation (PDF, PNG, JPG), local storage verification, size constraints, document linking per employee.
* **Profile Management**: Profile viewing and limited contact editing for employee role.

### Out-of-Scope
* Performance / Load / Stress Testing beyond standard local load.
* Cloud storage provider integrations (AWS S3, Azure Blob).
* Third-party SSO / OAuth integrations.

---

## 3. Test Environment

* **Application Name**: WorkForce HR
* **Backend Tech Stack**: Python 3.11+, FastAPI, SQLite, SQLAlchemy, JWT Authentication
* **Frontend Tech Stack**: HTML5, CSS3, JavaScript (ES6+), Jinja2 Templates
* **Automation Tools**: Playwright 1.40+, Pytest, pytest-html, pytest-xdist
* **Supported Browsers**: Google Chrome / Chromium, Mozilla Firefox, WebKit (Safari engine)
* **Base URL**: `http://127.0.0.1:8000`

---

## 4. Testing Types & Strategy

1. **Smoke Testing**: Verifying core application availability, login capabilities, and navigation after deployment.
2. **Functional Testing**: Validating business requirements for employee CRUD, document uploads, and profile updates.
3. **UI / Usability Testing**: Ensuring clean responsive layout, visible `data-testid` attributes, correct formatting, badges, and modals.
4. **Validation Testing**: Verifying error messaging on invalid inputs, missing fields, malformed dates, and duplicate entries.
5. **Negative Testing**: Attempting unauthorized access, submitting SQL/script strings, uploading unsupported file extensions (.exe, .txt).
6. **Role-Based Access Control (RBAC) Testing**: Verifying endpoint and UI element protection according to Admin, HR Manager, and Employee permissions.
7. **File Upload Testing**: Uploading valid PDF, PNG, JPG files and verifying extension blocking for disallowed MIME types.
8. **Regression Testing**: Automated execution of Playwright test suite on build changes.

---

## 5. Entry & Exit Criteria

### Entry Criteria
* Application backend (FastAPI) and SQLite database initialized and running cleanly.
* Seed data populated with 3 test accounts and 15+ employee records.
* Test plan and manual test cases reviewed and approved.

### Exit Criteria
* 100% of critical manual and automated test cases executed.
* 0 Critical or High severity open defects remaining.
* Playwright E2E test suite passing with HTML execution report generated.

---

## 6. Risks & Mitigation

| Risk | Impact | Mitigation Strategy |
| :--- | :--- | :--- |
| Test environment database dirty state causing test flakiness | High | Use Pytest fixtures and isolated SQLite DB setup/seed per test session. |
| Playwright async dynamic UI render delays | Medium | Utilize Playwright built-in auto-waiting and web-first assertions (`expect(locator).to_be_visible()`). |
| File upload storage permission failures | Low | Ensure `app/static/uploads` directory exists with write permissions during seed/startup. |

---

## 7. Assumptions

* Application runs locally on port 8000.
* Test users (`admin@workforce.test`, `hr@workforce.test`, `employee@workforce.test`) remain seeded and available.

# WorkForce HR — Playwright E2E Automation Framework

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-v1.40%2B-green.svg)](https://playwright.dev/python/)
[![Pytest](https://img.shields.io/badge/Pytest-v7.4%2B-orange.svg)](https://docs.pytest.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.100%2B-teal.svg)](https://fastapi.tiangolo.com/)

A realistic, enterprise-grade Employee Management System (**WorkForce HR**) paired with a complete End-to-End (E2E) Browser Automation Framework built using **Python 3.11+**, **Playwright**, **Pytest**, and the **Page Object Model (POM)** pattern.

This repository is built specifically as a **QA Automation / SDET Fresher Portfolio Project**, demonstrating practical skills in browser automation, role-based testing, file uploads, automated test reporting, failure trace analysis, and test architecture.

---

## 🌟 Key Capabilities Demonstrated

* **End-to-End Browser Automation**: Multi-browser test coverage (Chromium, Firefox, WebKit) using Playwright.
* **Page Object Model (POM)**: Clean abstraction of web pages and components separating test logic from DOM elements.
* **Role-Based Access Control (RBAC) Verification**: Isolated test sessions and permissions testing for **Admin**, **HR Manager**, and **Employee** roles.
* **Authentication State Reuse**: Reusable Playwright storage states (`playwright/.auth/`) for fast, session-cached test execution.
* **Data-Driven & Validation Testing**: Comprehensive boundary and negative testing (duplicate email checks, malformed phones/dates, non-numeric salaries, required fields).
* **File Upload Automation**: Automated file attachment handling (`set_input_files`) supporting PDF, PNG, and JPG documents with format validation.
* **Self-Contained Reporting & Failure Analysis**:
  * Rich HTML execution reports via `pytest-html`.
  * Automatic screenshot capture on test failure stored in `reports/screenshots/`.
  * Detailed ZIP trace logs for Playwright Trace Viewer debugging in `reports/traces/`.
* **Parallel Test Execution**: Independent test design enabling high-speed parallel execution via `pytest-xdist`.

---

## 📐 Framework Architecture

```text
               Pytest Test Runner
                      │
               Fixtures & Auth State
        (admin_page, hr_page, employee_page)
                      │
              Page Object Layer
  (LoginPage, DashboardPage, EmployeeListPage, etc.)
                      │
           Playwright Browser Engine
        (Chromium / Firefox / WebKit)
                      │
          WorkForce HR Application
            (FastAPI + SQLite DB)
                      │
        Web-First Assertions (expect API)
                      │
      ─────────────────────────────────
     │                                 │
HTML Report                     Screenshots & Traces
(playwright_report.html)        (reports/screenshots & traces)
```

---

## 📁 Repository Directory Structure

```text
WorkForce-HR-Playwright-Automation/
│
├── app/                        # WorkForce HR Web Application (FastAPI)
│   ├── main.py                 # FastAPI application entrypoint
│   ├── database.py             # SQLite & SQLAlchemy engine configuration
│   ├── models.py               # ORM Models (User, Employee, Document)
│   ├── schemas.py              # Pydantic schemas & input validation
│   ├── auth.py                 # JWT authentication & password hashing
│   ├── seed.py                 # Seed script (3 users, 15+ employees)
│   ├── routers/
│   │   └── pages.py            # Jinja2 template & endpoint routes
│   ├── static/                 # CSS styles, client JS, uploaded files
│   └── templates/              # HTML Jinja templates (base, login, employees, etc.)
│
├── automation/                 # Playwright + Pytest Test Framework
│   ├── config/
│   │   └── config.py           # Environment variables & constants
│   ├── pages/                  # Page Object Model classes
│   │   ├── base_page.py
│   │   ├── login_page.py
│   │   ├── dashboard_page.py
│   │   ├── employee_list_page.py
│   │   ├── employee_form_page.py
│   │   ├── employee_details_page.py
│   │   └── profile_page.py
│   ├── tests/                  # Automated test suites (39 tests)
│   │   ├── test_login.py
│   │   ├── test_dashboard.py
│   │   ├── test_employees.py
│   │   ├── test_employee_validation.py
│   │   ├── test_role_permissions.py
│   │   ├── test_file_upload.py
│   │   └── test_profile.py
│   ├── fixtures/
│   │   └── test_fixtures.py    # Pytest fixtures & auth state setup
│   ├── test_data/
│   │   └── employees.json      # Test dataset
│   ├── utils/                  # Helper utilities & failure screenshot generator
│   │   ├── helpers.py
│   │   └── screenshots.py
│   ├── conftest.py             # Root Pytest hooks & screenshot capture
│   └── pytest.ini              # Pytest default CLI flags
│
├── manual_testing/             # Manual QA Artifacts
│   ├── test_plan.md            # Comprehensive QA Test Plan
│   ├── test_cases.xlsx         # 45 Manual Test Cases spreadsheet
│   └── bug_reports.md          # 5 Realistic Bug Reports
│
├── reports/                    # Execution Artifacts
│   ├── screenshots/            # Failure screenshots
│   ├── traces/                 # Playwright ZIP traces
│   └── playwright_report.html  # Pytest HTML execution report
│
├── docs/
│   └── interview_questions.md  # Detailed SDET/QA interview Q&A guide
│
├── requirements.txt            # Root dependencies
└── README.md                   # Project documentation
```

---

## 🛠️ Installation & Setup Guide

### 1. Prerequisites
* **Python 3.11+** installed on your system.
* **Git** installed.

### 2. Clone Repository & Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/your-DJPATEL001/Employee-Management-System-Playwright-Automation.git
cd WorkForce-HR-Playwright-Automation

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows (PowerShell / Command Prompt):
venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers
```bash
playwright install
```

---

## 🚀 Running the Application

Start the local **WorkForce HR** web application server using Uvicorn:

```bash
python -m uvicorn app.main:app --port 8000 --reload
```

The application will launch at `http://127.0.0.1:8000`.

### 🔑 Test User Credentials

| Role | Email | Password | Allowed Capabilities |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@workforce.test` | `Admin@12345` | Full access (View, Add, Edit, Delete employees, Upload documents, Dashboard) |
| **HR Manager** | `hr@workforce.test` | `HR@12345` | Manage employees (View, Add, Edit, Upload documents). **Cannot** delete employees. |
| **Employee** | `employee@workforce.test` | `Employee@12345` | Self-service profile (View own profile/documents, update contact info). |

---

## 🧪 Running Automated Tests

Make sure the FastAPI server is running on `http://127.0.0.1:8000` before starting the test suite.

### Run All Automated Tests
```bash
python -m pytest
```

### Run Tests with Verbose Output & HTML Report
```bash
python -m pytest -v --html=reports/playwright_report.html --self-contained-html
```

### Run Tests in Parallel (`pytest-xdist`)
```bash
python -m pytest -n auto
```

### Run Specific Test Suite
```bash
python -m pytest automation/tests/test_login.py
```

---

## 🔍 Playwright Trace Viewer Debugging

When a test fails, Playwright captures a detailed ZIP trace. You can inspect network calls, DOM snapshots, console logs, and action timings using Playwright's built-in Trace Viewer:

```bash
playwright show-trace reports/traces/failed_test_name.zip
```

---

## 📊 Final Test Execution Metrics

| Category | Actual Count | Status |
| :--- | :--- | :--- |
| **Manual Test Cases** | 45 | Executed / Pass |
| **Automated Playwright Tests** | 39 | Executed / Pass |
| **Bug Reports Documented** | 5 | Logged & Reproducible |
| **Role Permissions Tested** | 3 Roles (Admin, HR, Employee) | Verified |

---

## 📜 License

This project is open-source and intended for educational and portfolio presentation purposes.

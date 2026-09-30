import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

# Test User Credentials
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@workforce.test")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Admin@12345")

HR_EMAIL = os.getenv("HR_EMAIL", "hr@workforce.test")
HR_PASSWORD = os.getenv("HR_PASSWORD", "HR@12345")

EMPLOYEE_EMAIL = os.getenv("EMPLOYEE_EMAIL", "employee@workforce.test")
EMPLOYEE_PASSWORD = os.getenv("EMPLOYEE_PASSWORD", "Employee@12345")

# Paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTH_DIR = os.path.join(ROOT_DIR, "playwright", ".auth")
REPORTS_DIR = os.path.join(os.path.dirname(ROOT_DIR), "reports")
SCREENSHOTS_DIR = os.path.join(REPORTS_DIR, "screenshots")
TRACES_DIR = os.path.join(REPORTS_DIR, "traces")

# Timeouts
DEFAULT_TIMEOUT = 10000  # 10s

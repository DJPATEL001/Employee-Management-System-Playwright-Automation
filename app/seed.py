from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models import User, Employee, Document
from app.auth import get_password_hash
import os
import shutil

def seed_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()

    try:
        # 1. Create Seed Users
        admin_user = User(
            name="System Admin",
            email="admin@workforce.test",
            password_hash=get_password_hash("Admin@12345"),
            role="Admin"
        )
        hr_user = User(
            name="Sarah Jenkins (HR)",
            email="hr@workforce.test",
            password_hash=get_password_hash("HR@12345"),
            role="HR Manager"
        )
        employee_user = User(
            name="John Doe",
            email="employee@workforce.test",
            password_hash=get_password_hash("Employee@12345"),
            role="Employee"
        )

        db.add_all([admin_user, hr_user, employee_user])
        db.commit()

        # 2. Create Seed Employees (15+)
        seed_employees_data = [
            {
                "employee_code": "EMP001",
                "first_name": "Alexander",
                "last_name": "Wright",
                "email": "alexander.wright@workforce.test",
                "phone": "9876543210",
                "department": "Engineering",
                "position": "Principal Architect",
                "joining_date": "2021-03-15",
                "salary": 125000.00,
                "status": "Active",
                "address": "101 Tech Boulevard, Suite 400, San Jose, CA"
            },
            {
                "employee_code": "EMP002",
                "first_name": "Sarah",
                "last_name": "Jenkins",
                "email": "sarah.jenkins@workforce.test",
                "phone": "9876543211",
                "department": "HR",
                "position": "HR Manager",
                "joining_date": "2020-01-10",
                "salary": 95000.00,
                "status": "Active",
                "address": "202 Human Resources Way, San Francisco, CA"
            },
            {
                "employee_code": "EMP003",
                "first_name": "John",
                "last_name": "Doe",
                "email": "employee@workforce.test",
                "phone": "9876543212",
                "department": "Engineering",
                "position": "Software Engineer",
                "joining_date": "2022-06-01",
                "salary": 85000.00,
                "status": "Active",
                "address": "742 Evergreen Terrace, Springfield, OR"
            },
            {
                "employee_code": "EMP004",
                "first_name": "Emily",
                "last_name": "Watson",
                "email": "emily.watson@workforce.test",
                "phone": "9876543213",
                "department": "Finance",
                "position": "Senior Financial Analyst",
                "joining_date": "2019-11-20",
                "salary": 98000.00,
                "status": "Active",
                "address": "404 Wall Street, New York, NY"
            },
            {
                "employee_code": "EMP005",
                "first_name": "Michael",
                "last_name": "Brown",
                "email": "michael.brown@workforce.test",
                "phone": "9876543214",
                "department": "Marketing",
                "position": "Marketing Lead",
                "joining_date": "2021-08-14",
                "salary": 90000.00,
                "status": "Active",
                "address": "88 Madison Ave, New York, NY"
            },
            {
                "employee_code": "EMP006",
                "first_name": "David",
                "last_name": "Miller",
                "email": "david.miller@workforce.test",
                "phone": "9876543215",
                "department": "Sales",
                "position": "Account Executive",
                "joining_date": "2023-01-15",
                "salary": 75000.00,
                "status": "Active",
                "address": "505 Commercial Lane, Austin, TX"
            },
            {
                "employee_code": "EMP007",
                "first_name": "Jessica",
                "last_name": "Taylor",
                "email": "jessica.taylor@workforce.test",
                "phone": "9876543216",
                "department": "Engineering",
                "position": "QA Lead",
                "joining_date": "2020-05-18",
                "salary": 92000.00,
                "status": "Active",
                "address": "12 Quality Drive, Seattle, WA"
            },
            {
                "employee_code": "EMP008",
                "first_name": "Robert",
                "last_name": "Wilson",
                "email": "robert.wilson@workforce.test",
                "phone": "9876543217",
                "department": "Engineering",
                "position": "DevOps Engineer",
                "joining_date": "2022-09-01",
                "salary": 96000.00,
                "status": "Active",
                "address": "909 Cloud Parkway, Portland, OR"
            },
            {
                "employee_code": "EMP009",
                "first_name": "Amanda",
                "last_name": "Garcia",
                "email": "amanda.garcia@workforce.test",
                "phone": "9876543218",
                "department": "HR",
                "position": "Recruitment Specialist",
                "joining_date": "2023-04-10",
                "salary": 68000.00,
                "status": "Active",
                "address": "303 Talent Street, Denver, CO"
            },
            {
                "employee_code": "EMP010",
                "first_name": "James",
                "last_name": "Martinez",
                "email": "james.martinez@workforce.test",
                "phone": "9876543219",
                "department": "Finance",
                "position": "Payroll Accountant",
                "joining_date": "2018-02-01",
                "salary": 72000.00,
                "status": "Inactive",
                "address": "707 Ledger Ave, Chicago, IL"
            },
            {
                "employee_code": "EMP011",
                "first_name": "Sophia",
                "last_name": "Anderson",
                "email": "sophia.anderson@workforce.test",
                "phone": "9876543220",
                "department": "Marketing",
                "position": "Content Strategist",
                "joining_date": "2022-11-05",
                "salary": 70000.00,
                "status": "Active",
                "address": "414 Creative Circle, Los Angeles, CA"
            },
            {
                "employee_code": "EMP012",
                "first_name": "Daniel",
                "last_name": "Thomas",
                "email": "daniel.thomas@workforce.test",
                "phone": "9876543221",
                "department": "Sales",
                "position": "Sales Director",
                "joining_date": "2017-09-12",
                "salary": 140000.00,
                "status": "Active",
                "address": "808 Enterprise Way, Boston, MA"
            },
            {
                "employee_code": "EMP013",
                "first_name": "Olivia",
                "last_name": "White",
                "email": "olivia.white@workforce.test",
                "phone": "9876543222",
                "department": "Engineering",
                "position": "Frontend Developer",
                "joining_date": "2023-02-28",
                "salary": 82000.00,
                "status": "Active",
                "address": "515 UI Street, San Diego, CA"
            },
            {
                "employee_code": "EMP014",
                "first_name": "William",
                "last_name": "Harris",
                "email": "william.harris@workforce.test",
                "phone": "9876543223",
                "department": "Finance",
                "position": "Chief Financial Officer",
                "joining_date": "2016-04-15",
                "salary": 185000.00,
                "status": "Active",
                "address": "1 Executive Plaza, New York, NY"
            },
            {
                "employee_code": "EMP015",
                "first_name": "Charlotte",
                "last_name": "Clark",
                "email": "charlotte.clark@workforce.test",
                "phone": "9876543224",
                "department": "HR",
                "position": "HR Coordinator",
                "joining_date": "2021-07-01",
                "salary": 60000.00,
                "status": "Inactive",
                "address": "222 Personnel Rd, Atlanta, GA"
            }
        ]

        employee_objs = [Employee(**emp) for emp in seed_employees_data]
        db.add_all(employee_objs)
        db.commit()

        # 3. Create Sample Document for Employee 3 (John Doe)
        uploads_dir = os.path.join(os.path.dirname(__file__), "static", "uploads")
        os.makedirs(uploads_dir, exist_ok=True)
        sample_doc_path = os.path.join(uploads_dir, "sample_resume_EMP003.pdf")
        with open(sample_doc_path, "wb") as f:
            f.write(b"%PDF-1.4 Sample Resume for John Doe (EMP003)")

        doc = Document(
            employee_id=employee_objs[2].id,
            file_name="John_Doe_Resume.pdf",
            file_path="uploads/sample_resume_EMP003.pdf",
            file_type="PDF"
        )
        db.add(doc)
        db.commit()

        print("Database seeded successfully with 3 users, 15 employees, and sample documents!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
